def get_confirmation(text, options = 2): #Options são entra quantas opções o usuário deve escolher
    while True:
        try:
            number = int(input(f'{text} '))   
            if 1 <= number <= options:
                return  number
            
            else:
                print(f'Please! Only NUMBERS from 1 to {options}.')
        except ValueError:
            print(f'Please! Only NUMBERS from 1 to {options}.')
                