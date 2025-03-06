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
        cur.execute("SELECT DISTINCT b.title, b.borrowed FROM book b LEFT JOIN author a ON a.id = b.id_author WHERE title LIKE ? OR a.name LIKE ?", (f'%{query}%', f'%{query}%'))
        books = cur.fetchall()
        
        return render_template("search.html", query=query, books=books)

    except:
        return render_template("error.html")
    
    finally:
        conn.close()