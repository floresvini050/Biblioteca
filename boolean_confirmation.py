from confirmation import get_confirmation

def boolean(message):
    if get_confirmation(message) == 1:
        return True
    else:
        return False