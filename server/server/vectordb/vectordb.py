from typing import Any, Dict, List, Optional, Sequence

from elasticsearch import Elasticsearch as ElasticsearchClient
from elasticsearch import NotFoundError
from pydantic import BaseModel

INDEX_NAME = "mlflow_embedding"


class DocEntry(BaseModel):
    """Represents a single document retrieved from Elasticsearch."""

    id: str
    # This is the raw content of the document. It may be json-serialized.
    content: str


class SearchResult(BaseModel):
    """Represents a single search result, corresponding to a single document.

    The higher the score, the more similar the document is to the query.
    """

    score: float
    content: DocEntry


class ElasticsearchVectorDB:
    def __init__(self) -> None:
        self.client = ElasticsearchClient(
            "http://localhost:9200",
            timeout=180,  # 3 minutes
        )

    def list_indexes(self) -> List[str]:
        return self.client.indices.get_alias(index="*").keys()  # type: ignore

    def get_doc_by_id(self, doc_id: str) -> Optional[DocEntry]:
        """Fetches a document from Elasticsearch by its ID.

        Parameters:
        - doc_id: The ID of the document to retrieve.

        Returns:
            A `DocEntry` object if found, otherwise `None`.
        """
        try:
            response = self.client.get(index=INDEX_NAME, id=doc_id)
            doc_source = response["_source"]
            return DocEntry(
                id=doc_source["id"],
                content=doc_source.get("text", ""),
            )
        except NotFoundError:
            print(f"Document with ID '{doc_id}' not found.")
            return None
        except Exception as e:
            print(f"Error fetching document with ID '{doc_id}': {e}")
            return None

    def vector_search(
        self,
        query_embedding: Sequence[float],
        limit: int = 5,
        threshold: Optional[float] = None,
    ) -> List[SearchResult]:
        """Performs a search over the given indexes for documents that are
        semantically similar to the given embedding vector.

        NOTE: This is hard-coded to search over the vectorDB INDEX_NAME, defined above.
        We've already set up this index with the appropriate documents, so you should
        not need to modify this.

        Parameters:
        - embedding: The embedding vector of the query document.
        - limit: The maximum number of search results to retrieve. Defaults to 5.
        - threshold: A minimum score threshold for returned documents. Documents
          with similarity scores below this threshold are not included. If None,
          no threshold is applied.

        Returns:
            The list of search results, sorted in descending order by their score.
        """
        if not self.client.indices.exists(index=INDEX_NAME):
            raise Exception(f"Index {INDEX_NAME} does not exist.")

        response = self.client.search(
            index=INDEX_NAME,
            knn={
                "field": "embedding",
                "query_vector": query_embedding,
                "num_candidates": limit * 20,
                "k": limit * 2,
            },
            min_score=threshold,
            size=limit * 2,
        )
        retrieved_docs: List[Dict[str, Any]] = [
            {**hit["_source"], "_score": hit["_score"]} for hit in response["hits"]["hits"]
        ]

        # Sort by score, keep the top `limit` candidates and return them as a list of SearchResults.
        retrieved_docs.sort(key=lambda x: x["_score"], reverse=True)

        search_results = [
            SearchResult(
                score=doc["_score"],
                content=DocEntry(
                    id=doc["id"],
                    content=doc["text"],
                ),
            )
            for doc in retrieved_docs
        ][:limit]

        return search_results
