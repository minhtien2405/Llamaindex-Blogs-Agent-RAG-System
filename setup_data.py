import os
import re
import pandas as pd
from dotenv import load_dotenv
from time import time
from qdrant_client import QdrantClient
from llama_index.core import Settings, Document, VectorStoreIndex, StorageContext
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.node_parser import SentenceSplitter

load_dotenv()

# Ensure necessary environment variables are set
required_env_vars = ['DATA_PATH', 'QDRANT_HOST', 'QDRANT_PORT', 'QDRANT_API_KEY', 'QDRANT_COLLECTION_NAME', 'OPENAI_API_KEY']
for var in required_env_vars:
    if os.getenv(var) is None:
        raise EnvironmentError(f"Environment variable {var} is not set.")

# Load the data
try:
    data = pd.read_csv(os.getenv('DATA_PATH'))
except Exception as e:
    raise RuntimeError(f"Error loading data from {os.getenv('DATA_PATH')}: {e}")

# Clean the text
def clean_text(text):
    """Clean and normalize text data."""
    text = re.sub(r'\s+', ' ', text)  # Replace multiple whitespace with a single space
    text = text.strip()  # Strip leading and trailing whitespace
    return text

data['title'] = data['title'].apply(clean_text)
data['content'] = data['content'].apply(clean_text)

# Initialize the Qdrant client
qdrant_client = QdrantClient(
    host=os.getenv('QDRANT_HOST'),
    port=os.getenv('QDRANT_PORT'),
    api_key=os.getenv('QDRANT_API_KEY'),
    timeout=60
)

# Attempt to delete the specified collection, ignore any errors
try:
    qdrant_client.delete_collection(os.getenv('QDRANT_COLLECTION_NAME'))
except Exception as e:
    print(f"Could not delete collection: {e}")

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI embedding
Settings.embedding = OpenAIEmbedding(model="text-embedding-3-small")

# Create Document objects from the DataFrame
documents = [
    Document(
        text=row['content'],
        metadata={
            'source': row['source'],
            'title': row['title'],
            'url': row['url'],
            'date': row['date'],
        },
    )
    for index, row in data.iterrows()
]

# Split documents into nodes for indexing
nodes = SentenceSplitter(
    chunk_size=256,
    chunk_overlap=128,
    paragraph_separator="\n\n",
).get_nodes_from_documents(documents)

# Initialize the Qdrant vector store
vector_store = QdrantVectorStore(
    client=qdrant_client,
    collection_name=os.getenv('QDRANT_COLLECTION_NAME'),
)

# Create a StorageContext using the vector store
storage_context = StorageContext.from_defaults(vector_store=vector_store)

print("Indexing started...")

# Create a VectorStoreIndex with the nodes and storage context
try:
    index = VectorStoreIndex(nodes, storage_context=storage_context)
except Exception as e:
    raise RuntimeError(f"Error during indexing: {e}")

# Output collection details
try:
    collections = qdrant_client.get_collections()
    print("Available collections:", collections)
    count = qdrant_client.count(
        collection_name=os.getenv('QDRANT_COLLECTION_NAME'),
        exact=True,
    )
    print(f"Document count in collection '{os.getenv('QDRANT_COLLECTION_NAME')}': {count}")
except Exception as e:
    print(f"Error retrieving collections or count: {e}")

# Completion message
print("Indexing completed successfully!")
