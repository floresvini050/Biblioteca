import csv
import sqlite3

# Conectar ao banco de dados
con = sqlite3.connect("books.db")
cur = con.cursor()

# Criar as tabelas, caso ainda não existam
cur.execute("""
CREATE TABLE IF NOT EXISTS author(
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           name VARCHAR(100) UNIQUE,
           quantity INTEGER DEFAULT 0);
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS book 
           (id INTEGER PRIMARY KEY AUTOINCREMENT, title VARCHAR(100), id_author INTEGER,
            borrowed INTEGER DEFAULT 0,
            borrower_name VARCHAR (100) DEFAULT NULL,
            loan_date DATE DEFAULT NULL,
            return_date DATE DEFAULT NULL,
            FOREIGN KEY (id_author) REFERENCES author(id));
""")

# Ler o arquivo CSV
with open('library.csv', encoding='utf-8') as csvfile:
    d = csv.DictReader(csvfile)
    for row in d:
        cur.execute("SELECT id, quantity FROM author WHERE name = ?", (row['author'],))
        author = cur.fetchone()

        if author is None:
            cur.execute('INSERT INTO author (name, quantity) VALUES (?, ?)', (row['author'], 1))
            author_id = cur.lastrowid
        else:
            author_id = author[0]
            current_quantity = author[1]
            new_quantity = current_quantity + 1
            cur.execute('UPDATE author SET quantity = ? WHERE id = ?', (new_quantity, author_id))
            
        cur.execute('INSERT INTO book (title, id_author) VALUES (?, ?)', (row['title'], author_id))

     

con.commit()
con.close()
