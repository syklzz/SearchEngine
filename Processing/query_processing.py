from Processing.file_processing import *
from Processing.matrix_processing import *


articles, titles = read_articles("Articles/corpus.txt")
processed_articles = process_articles(articles)
terms_dict, terms_freq = define_terms(processed_articles)
matrix = build_matrix(processed_articles, terms_dict)
processed_matrix = process_matrix(matrix)


def process_query(query, size):
    q = np.zeros(processed_matrix.shape[0])
    words = query.split()
    stemmer = PorterStemmer()
    for word in words:
        if word in terms_dict:
            q[terms_dict[stemmer.stem(word)]] = 1
    if np.sum(q > 0) == 0:
        return [], [], []
    q_norm = q / np.linalg.norm(q)
    result = q_norm.T @ processed_matrix
    result_dict = {}
    for i, c in enumerate(result):
        result_dict[i] = c
    result_sorted = dict(sorted(result_dict.items(), key=lambda item: item[1], reverse=True))
    d = []
    t = []
    p = []
    for i, doc in enumerate(result_sorted):
        t.append(titles[doc][:500])
        d.append(articles[doc][:500] + '...')
        p.append(doc)
        if i == size:
            break
    return d, t, p
