import sqlite3
from search_author import author_search
from search_title import title_search
from confirmation import get_confirmation
from returnbook import return_book

def main(): 
    # conectar com servidor sqlite
    try:
        con = sqlite3.connect("books.db")
        cur = con.cursor()
        
        while True:
            print('Hello, welcome to our library! How do you want to perform a search? ')

                # Selecionar tipo de busca ou fechar
            options_number = 4
            n = get_confirmation('Enter 1 to search by book title, 2 to search by author, 3 to return book and 4 to close: ', options_number)

            if n == 1:
                title = input('Enter the title of the book: ').strip().title()
                out = title_search(title, cur)

            elif n == 2:
                name = input('Enter the name of the author: ').strip().title()
                out = author_search(name, cur)
            elif n == 3:
                return_book()
            else:
                print('Closing...')
                break

            if out == False:
                break
    
    except:
        print('error connecting to database.')
        
    finally:
        print('Thank you for visiting our library! Come back often.')
        if 'con' in locals():
            con.commit()
            con.close()

main()
