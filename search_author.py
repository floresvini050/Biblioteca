from confirmation import get_confirmation
from loan import loan
from borrowed_verification import is_borrowed

def author_search(n, cur):
    cur.execute("SELECT id FROM author WHERE name LIKE ?", ('%' + n + '%',))
    found = cur.fetchone() # verificar se o autor está na lista

    if found is None: # Se não estiver
        
        number = int(input('We dont have any books by this author.'))
        if get_confirmation('Would you like to perform another search? [1 for yes / other for no]') == 1:
            return True
        return False
    
    else: #Se estiver
        cur.execute("Select book.title FROM book INNER JOIN author ON author.id = book.id_author WHERE book.id_author = ?", (found[0],))
        books = cur.fetchall()
        lenght = len(books)
        
        if lenght == 1: # Caso haja apenas um livro desse autor na biblioteca
            print(books[0][0]) 
 
            if get_confirmation('Do you want to borrow this book? [1 to yes/ 2 for no] ') == 1: # Se quiser, realizar o empréstimo
                if not is_borrowed(title, cur):
                    return False
                
                loan(books[0][0], cur)
                return False
            
            else: # Caso contrário, voltar ao iníxio
                if get_confirmation('Do you want to select another book? [1 for yes / other for no]') == 1:
                    return True
                return False
                    

        else: # Caso a biblioteca tiver mais de um livro desse autor
            print(f'We have {lenght} books by {n}:')

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
                    if not is_borrowed(title, cur):
                        loan(title, cur) # Realizar o empréstimo
                        return False
                    else:
                        if get_confirmation('This book is currently on loan. Do you want to select another one? [1 for yes / 2 for no] ') == 1:
                            return True
                        return False
            
                else:
                    print('Not found!') 
                    if get_confirmation('Do you want to select another book? [1 for yes/ other for no] ') == 1:
                        return True #Se a biblioteca nao tiver esse livro
                    return False
            else: # Se o leitor não quiser nenhum daqueles livros
                if get_confirmation('Would you like to perform another search? [1 for yes / other for no]') == 1:
                    return True
                return False