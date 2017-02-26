
# A very simple Flask Hello World app for you to get started with...

from flask import Flask,Blueprint, render_template, abort
from jinja2 import TemplateNotFound
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello from Flask!'

@app.route('/word_count')
def bokeh_render():
    return render_template('word_count.html')

@app.route('/sentiment_count')
def bokeh_sentiment_count():
    return render_template('sentiment_count.html')
