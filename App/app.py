from flask import Flask, render_template, request, redirect, url_for
from nltk.stem.porter import PorterStemmer
import numpy as np
from FileManager.file_manager import FileManager
from Matrix.matrix_builder import MatrixBuilder

app = Flask(__name__)

manager = FileManager("Articles/corpus.txt")
articles, titles = manager.read_articles()
processed_articles = manager.process_articles()
terms_dict, terms_freq = manager.define_terms(processed_articles)
builder = MatrixBuilder(processed_articles, terms_dict)
matrix = builder.process_matrix()


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        query = request.form['Query']
        if query == '':
            return f"Incorrect query. Try going to '/' to submit form again."
        return redirect(url_for('query', query=query))
    else:
        return f"The URL /search is accessed directly. Try going to '/' to submit form."


@app.route('/query/<query>/')
def query(query):
    size = 10
    q = np.zeros(matrix.shape[0])
    words = query.split()
    stemmer = PorterStemmer()
    for word in words:
        if word in terms_dict:
            q[terms_dict[stemmer.stem(word)]] = 1
    if np.sum(q > 0) == 0:
        return f"Incorrect query. Try going to '/' to submit form again."
    q_norm = q / np.linalg.norm(q)
    result = q_norm.T @ matrix
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
        if i == 10:
            break
    return render_template('documents.html', query=query, documents=d, titles=t, position=p, size=size)


@app.route('/info/<int:id>/', methods=['POST', 'GET'])
def info(id):
    return render_template('info.html', document=articles[id], title=titles[id])
