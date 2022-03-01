from flask import Flask, render_template, request, redirect, url_for
from Processing.query_processing import *

SIZE = 20
app = Flask(__name__)


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
    d, t, p = process_query(query, SIZE)
    if len(d) == 0:
        return f"Incorrect query. Try going to '/' to submit form again."
    return render_template('documents.html', query=query, documents=d, titles=t, position=p, size=SIZE)


@app.route('/info/<int:id>/', methods=['POST', 'GET'])
def info(id):
    return render_template('info.html', document=articles[id], title=titles[id])
