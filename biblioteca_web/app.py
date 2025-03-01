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
    search_type = request.form.get('search_type')
    query = request.form.get('query').strip().title()

    conn = database_connection()
    cur = conn.cursor() 

    if search_type == 'title_search':
        cur.execute("SELECT id FROM author WHERE name LIKE ?", ('%' + query + '%',))
        results = cur.fetchone()
        cur.execute("SELECT title FROM book where id = ?" (results, ))

    else:
        cur.execute("SELECT title FROM book WHERE title LIKE ?", ('%' + query + '%', ))
        results = cur.fetchall()

    conn.close()
    return render_template("search.html", results=results, query=query)  