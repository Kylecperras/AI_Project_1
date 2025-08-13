import chromadb
from chromadb.config import Settings

class Memory:
    def __init__(self, persist_directory="./memory"):
        self.client = chromadb.Client(Settings(persist_directory=persist_directory))
        self.collection = self.client.get_or_create_collection("conversation")

    def add(self, user_input, ai_response):
        self.collection.add(
            documents=[f"User: {user_input}\nAI: {ai_response}"],
            ids=[str(len(self.collection.get()['ids']))]
        )

    def search(self, query, n=3):
        results = self.collection.query(query_texts=[query], n_results=n)
        return results.get("documents", [])

