from confirmation import get_confirmation
from loan import loan
from borrowed_verification import is_borrowed

def title_search(t, cur):
    # Verificar se o nome do livro está no banco de dados
    cur.execute("""SELECT book.title, book.return_date, author.name 
                FROM book 
                INNER JOIN author 
                ON author.id = book.id_author
                WHERE title LIKE ?""", ('%' + t + '%',))
    found = cur.fetchall()


    # Caso não seja encontrado
    if not found:
        print("Sorry, we don't have the book you are looking for.")
        print('If you want, we can carry out a new search.')
        
        if get_confirmation('Would you like to perform another search? [1 for yes / other for no]') == 1:
            return True
        return False
    
    else:  
        author_name = found[0][2]
        print(f'The book you are looking for is {t} by {author_name}? ') # Se houver um livro com o nome que o usuário digitou no banco de dados, verificar se é o mesmo livro, conferindo o autor

        if get_confirmation('Is this the correct book? [1 for yes / 2 for no] ') == 1:
            if not is_borrowed(t, cur):
                print('We will proceed with your book loan!') # continuar caso seja o mesmo livro
                loan(t, cur)
                return False
            
            else:
                return get_confirmation('This book is currently on loan. Do you want to select another one?[1 for yes/ 2 for no]')
        
        if get_confirmation('Want to select a new book? [1 to yes/ 2 for no] ') == 1:# Caso contrário, realizar uma nova busca ou fechar o programa
            return True
        return False
            