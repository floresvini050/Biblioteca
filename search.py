import sqlite3

def main(): 
    # conectar com servidor sqlite
    con = sqlite3.connect("books.db")
    cur = con.cursor()
    
    while True:
        print('Hello, welcome to our library! How do you want to perform a search? ')

        while True:
            # Selecionar tipo de busca
            n = int(input('Enter 1 to search by book title, 2 to search by author: '))
            if n >= 1 and n <= 3:
                break

        if n == 1:
            title = input('Enter the title of the book: ')
            out = title_search(title, cur)

        elif n == 2:
            name = input('Enter the name of the author: ')
        
        else:
            print('Closing...')
            break

        if out == False:
            break


def title_search(t, cur):
    # Verificar se o nome do livro está no banco de dados
    cur.execute("SELECT title FROM book WHERE title = ?", (t,))
    found = cur.fetchone()[0]

    # Caso não seja encontrado
    if found is None:
        print("Sorry, we don't have the book you are looking for.")
        print('If you want, we can carry out a new search.')
        
        while True:
            # Perguntar ao usuário se quer prcourar outro livro
            number = int(input('Enter 1 to perform a new search, 2 to close: '))
            if number == 1 or number == 2:
                break
        if number == 1:
            return True
        
        else:
            return False # Caso contrário, finalizar o programa
    else:
        cur.execute("SELECT author.name FROM author INNER JOIN book ON author.id = book.id_author WHERE book.title = ?", (t,) )
        author_name = cur.fetchone()[0] 
        print(f'The book you are looking for is {t} by {author_name}? ') # Se houver um livro com o nome que o usuário digitou no banco de dados, verificar se é o mesmo livro, conferindo o autor

        while True:
            number = input('Enter 1 for yes, 2 for no: ')
            if number == 1 or number == 2:
                break

        if number == 1:
            print('We will proceed with your book loan!') # continuar caso seja o mesmo livro

        else:
            while True:
                number = int(input('Sorry, do you want to try a new search? [1 for yes/ 2 for no] '))
                if number == 1 or number == 2:
                    break # Caso contrário, realizar uma nova busca ou fechar o programa
            if number == 1:
                return True
            
            else:
                return False
        
main()