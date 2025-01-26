from confirmation import get_confirmation
from loan import loan

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