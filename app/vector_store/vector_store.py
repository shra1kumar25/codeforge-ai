import numpy as np


class VectorStore:

    def __init__(self):
        self.vectors = []
        self.documents = []

    def add(self, vector, document):
        self.vectors.append(np.array(vector))
        self.documents.append(document)

    def search(self, query_vector, top_k=3):
        if not self.vectors:
            return []

        query = np.array(query_vector)

        scores = []

        for index, vector in enumerate(self.vectors):
            similarity = np.dot(query, vector) / (
                np.linalg.norm(query) * np.linalg.norm(vector)
            )

            scores.append((similarity, self.documents[index]))

        scores.sort(reverse=True, key=lambda item: item[0])

        return scores[:top_k]
