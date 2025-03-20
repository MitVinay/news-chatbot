import chromadb
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import os
import pandas as pd
from huggingface_hub import login


class ChromaNewsVectorStore:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        self.hf_token = os.getenv('HF_TOKEN')
        self.data_path = "news-chatbot/data/processed/processed_news.csv"
        self.db_path = "news-chatbot/databases/news"
        self.model_name = "sentence-transformers/all-MiniLM-L6-v2"

        # Initialize Hugging Face login (optional)
        if self.hf_token:
            login(self.hf_token, add_to_git_credential=True)
            print("Login is successfull")

        # Initialize Chroma client and SentenceTransformer model
        self.client = chromadb.PersistentClient(path=self.db_path)
        self.model = SentenceTransformer(self.model_name)

        # Load data
        self.df = pd.read_csv(self.data_path)
        # Assuming 'Description' column has the text
        self.documents = self.df['Description'].tolist()

    def generate_embeddings(self):
        """Generate embeddings for the documents."""
        self.vectors = self.model.encode(self.documents).astype(float).tolist()
        print("Embedding Generated...")

    def prepare_metadata(self):
        """Prepare metadata for each document."""

        self.metadatas = [{
            "category": row['Category'],
            "sub_category": row['Sub_category'],
            "author": row['Author'],
            "published_date": row["Published_Date"],
            "link": row['Link'],
            "title": row['Title']
        } for _, row in self.df.iterrows()]
        print("Metadatas Generated...")

    def add_to_collection(self, collection_name: str):
        """Create or get collection and add documents to it."""
        # Create or get collection in Chroma
        collection = self.client.get_or_create_collection(name=collection_name)

        # Ensure 'ids' are unique for each document
        ids = [str(i) for i in range(len(self.documents))]

        # Add documents and vectors to the collection
        collection.add(
            ids=ids,
            documents=self.documents,
            embeddings=self.vectors,
            metadatas=self.metadatas
        )

        print(f"Data successfully added to the collection: {collection_name}")


# Usage example
if __name__ == "__main__":
    vector_store = ChromaNewsVectorStore()

    vector_store.generate_embeddings()
    vector_store.prepare_metadata()
    vector_store.add_to_collection("processed_news")
