from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def database_connection():
    conn = sqlite3.connect('books.db')
    conn.row_factory = sqlite3.Row #habilitar pesquisa por nomes de colunas
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods= ['POST'])
def search():
    seach_type = request.form['search_type']
    query = request.form['query'].strip().title()

    conn = database_connection()
    cur = conn.cursor
    