def get_confirmation(text):
    print(f'{text}',end=' ')
    while True:
        number = int(input())
        if number == 1:
            return True
        elif number == 2:
            return False
        else:
            print('Only option 1 and 2 are valid.')