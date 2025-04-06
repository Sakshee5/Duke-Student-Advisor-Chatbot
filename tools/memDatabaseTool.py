import os
import math
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from langchain_openai import OpenAIEmbeddings
from typing import List, Dict
import PyPDF2
import sys
from pathlib import Path

# Add the project root directory to the Python path
project_root = str(Path(__file__).parent.parent)
sys.path.append(project_root)

from utils.openai_utils import get_response

# Load API Key
load_dotenv()
pinecone_api_key = os.getenv("PINECONE_API_KEY")

# Initialize Pinecone client
pc = Pinecone(api_key=pinecone_api_key)

INDEX_NAME = "mem-database"
DIMENSION = 1536
METRIC = "cosine"
BATCH_SIZE = 100

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

def initialize_pinecone_index():
    """
    Creates or retrieves an existing Pinecone index and returns the index object.
    """
    existing_indexes = [index["name"] for index in pc.list_indexes()]
    
    if INDEX_NAME not in existing_indexes:
        print(f"Creating new Pinecone index: {INDEX_NAME}")
        pc.create_index(
            name=INDEX_NAME,
            dimension=DIMENSION,  # Model dimension
            metric=METRIC,        # Metric for similarity search
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )

    # Get index details and print the host URL
    index_info = pc.describe_index(INDEX_NAME)
    host_url = index_info['host']
    os.environ["PINECONE_INDEX_HOST_MEM"] = host_url

    print(f"Pinecone index host: {host_url}")

    # Connect to the index
    return pc.Index(INDEX_NAME, host=host_url)


def upsert_vectors(index, vectors, namespace="nutrition-text"):
    """
    Upserts vectors into the Pinecone index in batches, skipping if namespace already exists.
    """
    num_batches = math.ceil(len(vectors) / BATCH_SIZE)
    
    for i in range(num_batches):
        batch = vectors[i * BATCH_SIZE : (i + 1) * BATCH_SIZE]
        index.upsert(vectors=batch, namespace=namespace)
        print(f"Upserted batch {i+1}/{num_batches}")

    print(f"Successfully upserted {len(vectors)} vectors into Pinecone!")


def process_pdf(pdf_path: str, namespace: str) -> None:
    """
    Process a PDF file, extract text page by page, create embeddings and store in Pinecone
    """
    # Extract text from PDF page by page
    pages = _extract_text_from_pdf(pdf_path)
    
    # Create embeddings for each page
    vectors = []
    for page_num, page_text in enumerate(pages, start=1):
        # Split page text into chunks if needed
       
        embedding = embeddings.embed_query(page_text)
        vectors.append({
            'id': f"{namespace}-page{page_num}",
            'values': embedding,
            'metadata': {
                'text': page_text,
                'source': os.path.basename(pdf_path),
                'page_number': page_num,
                'pdf_path': pdf_path,
            }
        })
    
    # Store in Pinecone
    index = initialize_pinecone_index()
    upsert_vectors(index, vectors, namespace=namespace)

def _extract_text_from_pdf(pdf_path: str) -> List[str]:
    """
    Extract text from a PDF file, returning a list of page texts
    """
    pages = []
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            pages.append(page.extract_text())
    return pages

def delete_all_records(namespace: str = "mem-handbook"):
    """
    Deletes all vectors from the specified namespace in the Pinecone index.
    """
    index = initialize_pinecone_index()
    print(f"Deleting all vectors in namespace: '{namespace}'")
    
    index.delete(delete_all=True, namespace=namespace)
    
    print(f"All vectors deleted from namespace '{namespace}'.")



def search(query: str, top_k: int = 3, namespace: str = "mem-handbook") -> List[Dict]:
    """
    Search MEM related content in the vector database
    """
    # Create embedding for the query
    query_embedding = embeddings.embed_query(query)
    
    # Initialize index
    index = initialize_pinecone_index()
    
    # Search in Pinecone
    results = index.query(
        namespace=namespace,
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True
    )

    messages = [
        {"role": "system", "content": "You are a helpful assistant that summarizes text."},
        {"role": "user", "content": f"""Answer the following question based on the following text:
{results['matches']}

Question: {query}
"""}
    ]

    response = get_response(messages, os.getenv("OPENAI_API_KEY"))
    answer = response.content
    
    return answer


if __name__ == "__main__":

    pdf_path = "data/documents/MEM Student Handbook.pdf"
    namespace = "mem-handbook"
    
    # Process the PDF and create the database
    process_pdf(pdf_path, namespace)

    # delete_all_records(namespace)
    
    # Example search
    answer = search("What is the graduation requirements for MEM program?")
    print(answer)

