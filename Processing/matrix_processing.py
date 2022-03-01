import numpy as np


def build_matrix(processed_articles, terms):
    n = len(terms)
    m = len(processed_articles)
    matrix = np.zeros((n, m))
    for i in range(m):
        words = processed_articles[i].split()
        for j in range(len(words)):
            word = words[j]
            if word in terms:
                matrix[terms[word]][i] += 1
    return matrix


def process_matrix(matrix):
    n = matrix.shape[0]
    m = matrix.shape[1]
    matrix_processed = np.zeros((n, m))
    for i in range(n):
        matrix_processed[i] = matrix[i] * np.log(m / np.sum(matrix[i] != 0))
    return matrix_processed
