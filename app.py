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

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query').strip().title()

    try:

        conn = database_connection()
        cur = conn.cursor()

        books = []
        cur.execute("SELECT title, borrowed FROM book WHERE title LIKE ?", ('%' + query + '%',))
        results = cur.fetchall()
        for book in results:
            books.append(book)

        cur.execute("SELECT id FROM author WHERE name LIKE ?", ('%' + query + '%',))
        authors = cur.fetchall()
        
        if authors:
            author_ids = [author['id'] for author in authors]
            placeholders = ','.join(['?'] * len(author_ids))

            cur.execute(f"SELECT title, borrowed FROM book WHERE id_author IN ({placeholders})", author_ids)

            results = cur.fetchall()

            for book in results:
                books.append(book)
        
        return render_template("search.html", query=query, books=books)

    except:
        return("error.html")
    
    finally:
        conn.close()