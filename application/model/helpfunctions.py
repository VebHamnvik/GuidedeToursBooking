

# Testet
def check_two_passwords(password1, password2):
    if password1 == password2:
        return True
    else:
        return False

# Testet
def validate_username(username):
    if len(username) < 3:
        return False
    else:
        return True

#Testet
def validate_password(password):
    if len(password) < 5:
        return False
    else:
        return True




