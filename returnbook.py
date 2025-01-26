def return_book(cur):
    title = input('Enter the name of the book you want to return: ')
    cur.execute("UPDATE book SET borrowed = ?, date_loan, date_return WHERE title LIKE ? ", (0, None, None, '%' + title + '%'))

