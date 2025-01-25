import sqlite3
from datetime import date, timedelta

def main(): 
    # conectar com servidor sqlite
    try:
        con = sqlite3.connect("books.db")
        cur = con.cursor()
        
        while True:
            print('Hello, welcome to our library! How do you want to perform a search? ')

            while True:
                # Selecionar tipo de busca ou fechar
                n = int(input('Enter 1 to search by book title, 2 to search by author and 3 to close: '))
                if n >= 1 and n <= 3:
                    break

            if n == 1:
                title = input('Enter the title of the book: ').strip().title()
                out = title_search(title, cur)

            elif n == 2:
                name = input('Enter the name of the author: ').strip().title()
                out = author_search(name, cur)
            else:
                print('Closing...')
                break

            if out == False:
                break
    finally:
        if 'con' in locals():
            con.commit()
            con.close()

def title_search(t, cur):
    # Verificar se o nome do livro está no banco de dados
    cur.execute("SELECT title FROM book WHERE title LIKE ?", ('%' + t + '%',))
    found = cur.fetchone()

    # Caso não seja encontrado
    if found is None:
        print("Sorry, we don't have the book you are looking for.")
        print('If you want, we can carry out a new search.')
        
        return get_confirmation('Would you like to perform another search? [1 for yes / other for no]')
    else:
        cur.execute("SELECT author.name FROM author INNER JOIN book ON author.id = book.id_author WHERE book.title LIKE ?", ('%' + t + '%',) )
        author_name = cur.fetchone()[0] 
        print(f'The book you are looking for is {t} by {author_name}? ') # Se houver um livro com o nome que o usuário digitou no banco de dados, verificar se é o mesmo livro, conferindo o autor

        if get_confirmation('Is this the correct book? [1 for yes / 2 for no]'):
            print('We will proceed with your book loan!') # continuar caso seja o mesmo livro
            loan(t, cur)
            return False
        
        return False # Caso contrário, realizar uma nova busca ou fechar o programa
            
            
def author_search(n, cur):
    cur.execute("SELECT id FROM author WHERE name LIKE ?", ('%' + n + '%',))
    found = cur.fetchone() # verificar se o autor está na lista

    if found is None: # Se não estiver
        
        number = int(input('We dont have any books by this author.'))
        return get_confirmation('Would you like to perform another search? [1 for yes / other for no]')
    
    else: #Se estiver
        cur.execute("Select book.title FROM book INNER JOIN author ON author.id = book.id_author WHERE book.id_author = ?", (found[0],))
        books = cur.fetchall()
        lenght = len(books)
        
        if lenght == 1: # Caso haja apenas um livro desse autor na biblioteca
            print(books[0][0]) 
 
            if get_confirmation('Do you want to borrow this book? [1 to yes/ 2 for no] '): # Se quiser, realizar o empréstimo
                loan(books[0][0], cur)
                return False
            
            else: # Caso contrário, voltar ao iníxio
                return get_confirmation('Do you want to select another book? [1 for yes / other for no]')
                    

        else: # Caso a biblioteca tiver mais de um livro desse autor
            print(f'we have {lenght} books by {n}:')

            for c, book in enumerate(books): # Imprimir os livros do autor
                print(f'{book[0]}',end='')
                if c < lenght - 2:
                    print(', ',end='')
                elif c == lenght - 2:
                    print(' e ',end='')
                else:
                    print('.')

            while True: # Confirmar se o leitor quer algum desses livros
                number = int(input('Do you want to borrow any of these books? [1 for yes/ 2 for no] '))
                if number == 1 or number == 2:
                    break

            if number == 1: # Se quiser
                title = input('Which book do you want to borrow? ').strip().title() # Escolher o livro
                if title in [book[0] for book in books]:
                    loan(title, cur) # Realizar o empréstimo
                    return False
            
                else:
                    print('Not found!') 
                    return get_confirmation('Do you want to select another book? [1 for yes/ other for no] ') #Se a biblioteca nao tiver esse livro
            else: # Se o leitor não quiser nenhum daqueles livros
                return get_confirmation('Would you like to perform another search? [1 for yes / other for no]')
            
def loan(title, cur):
    while True:
        decision = int(input(f'You selected the book {title} Do you want to continue?. [1 to yes/ other for no]'))
        if decision == 1 or decision == 2:
            break
    if decision == 2:
        return False
    
    name = input("What is your name?: ").strip().title()

    today = date.today()
    today2 =  today.strftime('%d/%m/%Y')

    return_d = today + timedelta(15)
    return_d2 = return_d.strftime('%d/%m/%Y')

    cur.execute("UPDATE book SET borrowed = ?, borrower_name = ?, loan_date = ?, return_date = ? WHERE title like ? ", (1, name, today2, return_d2, '%' + title + '%')) #Atualizar os valores no banco de dados

    print(f'You must return or renew the book by {return_d2}.')
    
def get_confirmation(text):
    print(text)
    while True:
        number = int(input())
        if number == 1:
            return True
        elif number == 2:
            return False
        else:
            print('Only option 1 and 2 are valid.')

    
    
main()