import chromadb
import numpy as np
import random


class Highlights:
    def __init__(self, db_path="news-chatbot/databases/news", collection_name="processed_news", distance_threshold=0.2):
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_or_create_collection(
            name=collection_name)
        self.distance_threshold = distance_threshold
        self.all_items = self.collection.get(
            include=['embeddings', 'documents', 'metadatas'])
        self.vectors = np.array(self.all_items['embeddings'])
        self.documents = self.all_items['documents']
        self.categories = [metadata['category']
                           for metadata in self.all_items['metadatas']]
        self.final_frequency = {}

        # Create a dictionary where the key is the category and the value is a list of dictionaries
        self.category_documents = {}

        for metadata, document in zip(self.all_items['metadatas'], self.all_items['documents']):
            category = metadata['category']
            # If the category doesn't exist in the dictionary, create a list for it
            if category not in self.category_documents:
                self.category_documents[category] = []
            # Append the metadata and document as a dictionary
            self.category_documents[category].append({
                "metadata": metadata,
                "document": document
            })

    def find_similar_vectors(self):
        for item_id, embedding in zip(self.all_items["ids"], self.all_items["embeddings"]):
            results = self.collection.query(
                query_embeddings=[embedding],
                n_results=100
            )
            ids = [item_id]
            frequency = 0
            for neighbor_id, distance in zip(results["ids"][0], results["distances"][0]):
                if neighbor_id != item_id and distance <= self.distance_threshold:
                    frequency += 1
                    ids.append(neighbor_id)
            if frequency > 0:
                if frequency not in self.final_frequency:
                    self.final_frequency[frequency] = []
                self.final_frequency[frequency].append(ids)

    def filter_frequency(self, min_frequency=3):
        filtered_frequency = {}
        for freq, ids_list in self.final_frequency.items():
            if freq > min_frequency:
                unique_ids_set = []
                for ids in ids_list:
                    ids_set = set(ids)
                    if ids_set not in unique_ids_set:
                        unique_ids_set.append(ids_set)
                filtered_frequency[freq] = unique_ids_set
        # Convert sets back to lists
        self.filtered_frequency = {
            freq: [list(ids_set) for ids_set in ids_list]
            for freq, ids_list in filtered_frequency.items()
        }

    def get_highlights(self):
        self.find_similar_vectors()
        self.filter_frequency()
        output = []
        for count, vector_idss in self.filtered_frequency.items():
            for vector_ids in vector_idss:
                vector_id = random.choice(vector_ids)
                try:
                    index = self.all_items["ids"].index(vector_id)
                    metadata = self.all_items["metadatas"][index]
                    document = self.all_items["documents"][index]
                    output.append({
                        "id": vector_id,
                        "frequency": count,
                        "document": document,
                        "metadata": metadata
                    })
                except ValueError:
                    continue
        return output


# Usage example (in your Flask app, you would import this class)
if __name__ == "__main__":
    checker = Highlights()
    result = checker.get_highlights()
    print(result)
    for item in result:
        print(item)
