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
    query = request.form.get('query').strip()

    if not query:
       return render_template('index.html', error='Digite um termo para pesquisar')
    try:
        with database_connection() as conn:

            cur = conn.cursor()
            cur.execute("SELECT DISTINCT b.title, b.borrowed FROM book b LEFT JOIN author a ON a.id = b.id_author WHERE title LIKE ? COLLATE NOCASE OR a.name LIKE ? COLLATE NOCASE", (f'%{query}%', f'%{query}%'))
            books = cur.fetchall()
            
            return render_template("search.html", query=query, books=books)

    except sqlite3.Error as e:
        return render_template("error.html", message= 'Ocorreu um erro ao acessar o banco de dados')
    except Exception as e:
        return render_template("error.html", message='Ocorreu um erro inesperado')