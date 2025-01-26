from datetime import date, timedelta

def loan(title, cur):
    while True:
        decision = int(input(f"You selected the book '{title}' Do you want to continue?. [1 to yes/ other for no] "))
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

    print(f'Enjoy reading {title}.')

    print(f'You must return or renew the book by {return_d2}.')