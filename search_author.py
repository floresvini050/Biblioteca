from boolean_confirmation import boolean
from loan import loan
from borrowed_verification import is_borrowed

def author_search(n, cur):
    cur.execute("SELECT id FROM author WHERE name LIKE ?", ('%' + n + '%',))
    found = cur.fetchone() # verificar se o autor está na lista

    if found is None: # Se não estiver
        
        print('We dont have any books by this author.')
        return boolean('Would you like to perform another search? [1 for yes / other for no] ') 
    
    else: #Se estiver
        cur.execute("Select book.title FROM book INNER JOIN author ON author.id = book.id_author WHERE book.id_author = ?", (found[0],))
        books = cur.fetchall()
        lenght = len(books)
        if lenght == 1:
             print(f'We have one book by {n}.')
        else:
            print(f'We have {lenght} books by {n}:')

        for c, book in enumerate(books): # Imprimir os livros do autor
            print(f'{book[0]}',end='')
            if c < lenght - 2:
                print(', ',end='')
            elif c == lenght - 2:
                print(' e ',end='')
            else:
                print('.')

           
        title = input('Which book do you want to borrow? ').strip().title() # Escolher o livro
        if not title:
            print('Please, enter the name of the book.')

        elif title in [book[0] for book in books]:
            if not is_borrowed(title, cur):
                loan(title, cur) # Realizar o empréstimo
                return False
                
            else:
                return boolean('This book is currently on loan. Do you want to select another one? [1 for yes / 2 for no] ')
                
        else:
            print('Not found!') 
            return boolean('Do you want to select another book? [1 for yes/ other for no] ')
                            

                    