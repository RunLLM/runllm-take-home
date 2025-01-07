import json
from typing import List
from server.llm.ollama_client import OllamaClient

# Initialize the Ollama client with the nomatic embeddings model
embedding_client = OllamaClient()

def generate_embedding(text: str) -> List[float]:
    """Generate embedding for the given text using Ollama client."""
    response = embedding_client.embed([text])
    return response[0]

def process_documents(input_file: str, output_file: str):
    """
    Read documents from input JSON file, generate embeddings, and write to output JSON file
    in a format suitable for Elasticsearch bulk upload.
    """
    with open(input_file, 'r') as infile:
        documents = json.load(infile)

    bulk_data = []

    for doc in documents:
        text = doc.get("text")
        doc_id = doc.get("id")

        # Generate embedding for the text
        embedding = generate_embedding(text)

        # Create Elasticsearch bulk upload format
        bulk_data.append({"index": {"_id": doc_id}})
        bulk_data.append({"id": doc_id, "text": text, "embedding": embedding})

    # Write bulk data to output file
    with open(output_file, 'w') as outfile:
        for entry in bulk_data:
            outfile.write(json.dumps(entry) + "\n")

if __name__ == "__main__":
    input_file = "texts.json"
    output_file = "embeddings.json"

    process_documents(input_file, output_file)
    print(f"Processed documents saved to {output_file}")