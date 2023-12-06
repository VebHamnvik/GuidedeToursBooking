from application.model.helpfunctions import check_two_passwords, validate_username, validate_password
from application import create_app

# Tester krav 1.2.1
def test_check_two_identical_passwords_gets_validated():
    pass1 = "Testpassword"
    pass2 = "Testpassword"

    assert check_two_passwords(pass1, pass2)

# Tester krav 1.2.1
def test_two_different_passwords_doesnt_get_validated():
    pass1 = "Testpassord"
    pass2 = "testpassord"

    assert not check_two_passwords(pass1, pass2)

def test_long_enough_username_gets_validated():
    username = "Validated"

    assert validate_username(username)

def test_not_long_enough_username_doesnt_get_validated():
    username = "Hi"

    assert not validate_username(username)

# Tester krav 11.1.2
def test_long_enough_password_gets_validated():
    password = "Testpassword"

    assert validate_password(password)

# Tester krav 11.1.2
def test_password_just_on_the_border_doesnt_get_validated():
    password = "1234"

    assert not validate_password(password)

# Tester krav 11.1.2
def test_not_long_enough_password_doesnt_get_validated():
    password = "Hi"

    assert not validate_password(password)

# Tester krav 7.0 - 7.4.1
def test_create_app_with_default_config():
    app = create_app()
    database = app.config['DATABASE_URI']

    assert app is not None
    assert database == 'application/final_database.db'

# Tester krav 7.0 - 7.4.1
def test_create_app_with_production_config():
    app = create_app(config_name='production')
    database = app.config['DATABASE_URI']

    assert app is not None
    assert database == 'application/final_database.db'

# Tester krav 7.0 - 7.4.1
def test_create_app_with_testing_config():
    app = create_app(config_name='testing')
    database = app.config['DATABASE_URI']

    assert app is not None
    assert database == 'test_db.db'