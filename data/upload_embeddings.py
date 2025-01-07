import json
import time
from elasticsearch import Elasticsearch, helpers
from server.llm.ollama_client import NUM_DIMENSIONS

# Initialize the Elasticsearch client
es = Elasticsearch(
    "http://localhost:9200",
    request_timeout=180,
)

# Function to wait for Elasticsearch to become available
def wait_for_es(timeout: int, interval: int):
    """Wait for Elasticsearch to become available."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            if es.ping():
                print("Elasticsearch is up and running.")
                return
        except ConnectionError:
            pass
        print("Waiting for Elasticsearch to be ready...")
        time.sleep(interval)
    raise Exception("Elasticsearch did not become available in time.")

# Index settings and mappings
def create_index(index_name):
    """Create an Elasticsearch index with the appropriate mapping for embeddings."""
    if es.indices.exists(index=index_name):
        print(f"Index '{index_name}' already exists, skipping creation.")
        return

    body = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 1
        },
        "mappings": {
            "properties": {
                "content": {
                    "type": "text",
                    "analyzer": "standard"
                },
                "embedding": {
                    "type": "dense_vector",
                    "dims": NUM_DIMENSIONS,
                    "index": True,
                    "similarity": "dot_product",
                }
            }
        }
    }

    es.indices.create(index=index_name, body=body)
    print(f"Index '{index_name}' created successfully.")


# Bulk upload data to Elasticsearch
def bulk_upload(index_name, data_file):
    """Upload data from a JSON file to Elasticsearch in bulk."""
    with open(data_file, 'r') as file:
        actions = [
            {
                "_index": index_name,
                "_id": entry["id"],
                "_source": entry
            }
            for line in file
            if (entry := json.loads(line)) and "index" not in entry
        ]

        helpers.bulk(es, actions)
        print(f"Successfully uploaded data to index '{index_name}'.")


if __name__ == "__main__":
    index_name = "mlflow_embedding"
    data_file = "data/embeddings.json"

    # Wait for Elasticsearch to be ready
    wait_for_es(timeout=120, interval=5)

    create_index(index_name)
    bulk_upload(index_name, data_file)
