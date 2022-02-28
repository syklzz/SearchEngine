import numpy as np


class MatrixBuilder:
    def __init__(self, articles, terms):
        self.articles = articles
        self.terms = terms

    def build_matrix(self):
        n = len(self.terms)
        m = len(self.articles)
        matrix = np.zeros((n, m))
        for i in range(m):
            words = self.articles[i].split()
            for j in range(len(words)):
                word = words[j]
                if word in self.terms:
                    matrix[self.terms[word]][i] += 1
        return matrix

    def process_matrix(self):
        matrix = self.build_matrix()
        n = matrix.shape[0]
        m = matrix.shape[1]
        matrix_processed = np.zeros((n, m))
        for i in range(n):
            matrix_processed[i] = matrix[i] * np.log(m / np.sum(matrix[i] != 0))
        return matrix_processed

