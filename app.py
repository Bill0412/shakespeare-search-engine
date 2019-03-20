from flask import Flask, render_template, request

from query import query

result = []

app = Flask(__name__)


@app.route('/')
def index():
    search_term = request.form.get('search-box')
    # only one word supported
    links = query(search_term)

    return render_template("index.html", links)


