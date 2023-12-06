
import pytest
from bs4 import BeautifulSoup
from flask.testing import FlaskClient
from flask_login import login_user
from flask import request

from application import create_app
from application.model.database import create_connection, create_tables, connect_to_db, drop_tables
from application.model.dbuser import insert_user_info_to_db, get_user_by_id
from application.model.user import User
from test_fixtures import connect_test_db



@pytest.fixture
def app():
    app = create_app(config_name='testing')
    conn = create_connection(app.config['DATABASE_URI'])
    create_tables(conn)

    yield app

    with app.app_context():
        drop_tables(conn)
        conn.close()

@pytest.fixture
def client(app) -> FlaskClient:
    client = app.test_client()
    return client


# Tester krav 1.1 og 9.1.1
def test_getting_to_register_page_for_not_logged_in_users(client: FlaskClient):
    with client.application.test_request_context():
        response = client.get('/registrer')

        assert response.status_code == 200
        assert b'Registrer ny bruker' in response.data
        assert b'Brukernavn' in response.data

# Tester krav 1.1 og 9.1.1
def test_registering_a_new_user_with_register_api(client: FlaskClient):
    with client:
        url = 'http://127.0.0.1:5000/registrer'
        data = {
            "username": "Testnavn",
            "password": "Testpassord",
            "password2": "Testpassord",
            "email": "email@gmail.com"
        }

        response = client.post(url, data=data)
        assert response.status_code == 302

# Tester krav 1.1 og 9.1.1
def test_check_new_user_through_api_is_same_in_database_register(client: FlaskClient, connect_test_db):
    conn, cur = connect_test_db
    with client:
        url = 'http://127.0.0.1:5000/registrer'
        data = {
            "username": "Testnavn",
            "password": "Testpassord",
            "password2": "Testpassord",
            "email": "email@gmail.com"
        }

        response = client.post(url, data=data)

        assert response.status_code == 302

        user = get_user_by_id(cur, 1)
        assert user.username == "Testnavn"
        assert user.password == "Testpassord"
        assert user.email == "email@gmail.com"

def test_check_if_it_redirects_to_corrects_page_after_registering_a_new_user_register(client: FlaskClient):
    with client:
        url = 'http://127.0.0.1:5000/registrer'
        data = {
            "username": "Testnavn",
            "password": "Testpassord",
            "password2": "Testpassord",
            "email": "email@gmail.com"
        }

        response = client.post(url, data=data)
        location_header = response.headers.get('Location')

        assert response.status_code == 302
        assert location_header == '/login'

# Tester krav 1.1 og 9.1.1
def test_flash_message_when_already_taken_username_register(client: FlaskClient, connect_test_db):
    conn, cur = connect_test_db
    insert_user_info_to_db(conn, cur, "Testnavn", "Testpassord", "epost@gmail.com")
    url = '/registrer'

    data = {
        "username": "Testnavn",
        "password": "Testpassord",
        "password2": "Testpassord",
        "email": "email@gmail.com"
    }

    with client:
        response = client.post(url, data=data)

        assert response.status_code == 200
        assert b'Brukernavnet er allerede i bruk' in response.data

# Tester krav 1.1 og 9.1.1
def test_flash_message_when_username_is_not_input_register(client: FlaskClient):
    url = '/registrer'
    data = {
        "username": "",
        "password": "Testpassord",
        "password2": "Testpassord",
        "email": "email@gmail.com"
    }

    with client:
        response = client.post(url, data=data)
        assert response.status_code == 200
        assert b'Brukernavn kreves!' in response.data

# Tester krav 1.1 og 9.1.1
def test_flash_message_when_username_is_not_loger_than_3_symbols_register(client: FlaskClient):
    url = '/registrer'
    data = {
        "username": "AB",
        "password": "Testpassord",
        "password2": "Testpassord",
        "email": "email@gmail.com"
    }

    with client:
        response = client.post(url, data=data)
        assert response.status_code == 200
        assert b'Vennligst skriv ett brukernavn som er lengre enn' in response.data

# Tester krav 1.1 og 9.1.1
def test_flash_message_when_password1_is_not_input_register(client: FlaskClient):
    url = '/registrer'
    data = {
        "username": "Testnavn",
        "password": "",
        "password2": "Testpassord",
        "email": "email@gmail.com"
    }

    with client:
        response = client.post(url, data=data)
        assert response.status_code == 200
        assert b'Passord kreves!' in response.data

# Tester krav 1.1 og 9.1.1
def test_flash_message_when_password2_is_not_input_register(client: FlaskClient):
    url = '/registrer'
    data = {
        "username": "Testnavn",
        "password": "Testpassord",
        "password2": "",
        "email": "email@gmail.com"
    }

    with client:
        response = client.post(url, data=data)
        assert response.status_code == 200
        assert b'Passord kreves!' in response.data

# Tester krav 1.1, 11.1.2, og 9.1.1
def test_flash_message_when_password_is_less_than_5_symbols_register(client: FlaskClient):
    url = '/registrer'
    data = {
        "username": "Testnavn",
        "password": "Test",
        "password2": "Test",
        "email": "email@gmail.com"
    }

    with client:
        response = client.post(url, data=data)
        assert response.status_code == 200
        assert b'Vennligst skriv et passord som er lengre enn 4' in response.data

# Tester krav 1.1 og 9.1.1
def test_flash_message_when_email_is_not_input_register(client: FlaskClient):
    url = '/registrer'
    data = {
        "username": "Testnavn",
        "password": "Testpassord",
        "password2": "Testpassord",
        "email": ""
    }

    with client:
        response = client.post(url, data=data)
        assert response.status_code == 200
        assert b'Email kreves' in response.data

# Tester krav 1.1 og 9.1.1
def test_flash_message_when_passwords_doesnt_match_register(client: FlaskClient):
    url = '/registrer'
    data = {
        "username": "Testnavn",
        "password": "Testpassord",
        "password2": "Testpassord2",
        "email": "email@gmail.com"
    }

    with client:
        response = client.post(url, data=data)
        assert response.status_code == 200
        assert b'Passordene matcher ikke!' in response.data

# Tester krav 1.1 og 9.1.1
def test_user_not_being_put_into_the_database_if_input_is_not_correct(client:FlaskClient, connect_test_db):
    conn, cur = connect_test_db
    url = '/registrer'
    data = {
        "username": "",
        "password": "Testpassord",
        "password2": "Testpassord2",
        "email": "email@gmail.com"
    }

    with client:
        response = client.post(url, data=data)
        user = get_user_by_id(cur, 1)

        assert user is None

def test_getting_to_loing_page_for_not_logged_in_users(client: FlaskClient):
    with client.application.test_request_context():
        response = client.get('/login')

        assert response.status_code == 200
        assert b'Logg inn' in response.data
        assert b'Brukernavn' in response.data
        assert b'Passord' in response.data

# Tester krav 1.2.1
def test_flash_message_when_username_not_input_login(client: FlaskClient):
    url = '/login'
    data = {
        "username": "",
        "password": "Testpassord"
    }
    with client:
        response = client.post(url, data=data)
        assert response.status_code == 200
        assert b'Brukernavn kreves' in response.data

# Tester krav 1.2.1
def test_flash_message_when_password_not_input_login(client: FlaskClient):
    url = '/login'
    data = {
        "username": "Testpassord",
        "password": ""
    }
    with client:
        response = client.post(url, data=data)
        assert response.status_code == 200
        assert b'Passord kreves' in response.data

# Tester krav 1.2.1
def test_if_username_doesnt_match_with_an_entry_in_the_database_login(client: FlaskClient, connect_test_db):
    conn, cur = connect_test_db
    insert_user_info_to_db(conn, cur, "Testnavn", "Testpassord", "epost@gmail.com")
    url = '/login'
    data = {
        "username": "Testnavn2",
        "password": "Testpassord"
    }
    with client:
        response = client.post(url, data=data)
        assert response.status_code == 200
        assert b'Feil brukernavn eller passord' in response.data

# Tester krav 1.2.1
def test_if_password_doesnt_match_with_an_entry_in_the_database_login(client: FlaskClient, connect_test_db):
    conn, cur = connect_test_db
    insert_user_info_to_db(conn, cur, "Testnavn", "Testpassord", "epost@gmail.com")
    url = '/login'
    data = {
        "username": "Testnavn",
        "password": "Testpassord2"
    }
    with client:
        response = client.post(url, data=data)
        assert response.status_code == 200
        assert b'Feil brukernavn eller passord' in response.data

# Tester krav 1.2.1
def test_successful_login(client: FlaskClient, connect_test_db):
    conn, cur = connect_test_db
    insert_user_info_to_db(conn, cur, "Testnavn", "Testpassord", "epost@gmail.com")
    url = '/login'
    data = {
        "username": "Testnavn",
        "password": "Testpassord"
    }
    with client:
        response = client.post(url, data=data)
        assert response.status_code == 302


def test_my_profile_is_authenticated(client: FlaskClient):
    user = User(1, "Testnavn", "Testpassord", "Epost@gmail.com")

    with client.application.test_request_context():
        login_user(user)

        response = client.get('/my_profile')

        assert response.status_code == 200
        assert b'Brukernavn:' in response.data
        assert b'Epost:' in response.data

def test_my_profile_is_not_authenticated(client: FlaskClient):
    with client.application.test_request_context():
        response = client.get('/my_profile')

        assert response.status_code == 401
        assert b'Authentication required for this API endpoint' in response.data


def test_link_to_change_profile_works_from_my_profile(client: FlaskClient):
    user = User(1, "Testnavn", "Testpassord", "Epost@gmail.com")

    with client.application.test_request_context():
        login_user(user)

        response = client.get('/my_profile')

        assert response.status_code == 200
        assert b'<a href="change_profile">' in response.data

        soup = BeautifulSoup(response.data, 'html.parser')
        link = soup.find('a', href='change_profile')

        assert link is not None
        link_url = link['href']

        link_response = client.get(link_url)

        assert link_response.status_code == 200
        assert b'Endre profilen din' in link_response.data

def test_link_to_change_password_works_from_my_profile(client: FlaskClient):
    user = User(1, "Testnavn", "Testpassord", "Epost@gmail.com")

    with client.application.test_request_context():
        login_user(user)

        response = client.get('/my_profile')

        assert response.status_code == 200
        assert b'<a href="change_profile">' in response.data

        soup = BeautifulSoup(response.data, 'html.parser')
        link = soup.find('a', href='change_password')

        assert link is not None
        link_url = link['href']

        link_response = client.get(link_url)

        assert link_response.status_code == 200
        assert b'Endre passordet ditt:' in link_response.data

# Tester krav 1.3.1, 1.3.2, og 1.3.4
def test_change_profile_with_new_information(client: FlaskClient, connect_test_db):
    conn, cur = connect_test_db
    insert_user_info_to_db(conn, cur, "Testnavn", "Testpassord", "epost@gmail.com")
    user = User(1, "Testnavn", "Testpassord", "Epost@gmail.com")

    with client.application.test_request_context():
        login_user(user)

        url = 'change_profile'
        data = {
            "username": "Testnavn2",
            "email": "email@gmail.com",
            "description": "Testdesc",
            "birthdate": "i fjor",
            "gender": "x"
        }

        response = client.post(url, data=data)
        assert response.status_code == 200

        user_after = get_user_by_id(cur, 1)
        assert user_after.username == "Testnavn2"
        assert user_after.email == "email@gmail.com"
        assert user_after.description == "Testdesc"
        assert user_after.birthdate == "i fjor"
        assert user_after.gender == "x"

# Tester krav 1.3.1, 1.3.2, og 1.3.4
def test_not_changing_user_information_by_leaving_blank_lines(client: FlaskClient, connect_test_db):
    conn, cur = connect_test_db
    insert_user_info_to_db(conn, cur, "Testnavn", "Testpassord", "epost@gmail.com", "Testdesc", "i fjor", "x")
    user_before = get_user_by_id(cur, 1)

    with client.application.test_request_context():
        login_user(user_before)

        url = 'change_profile'
        data = {
            "username": "Testnavn2",
            "email": "email@gmail.com",
            "description": "",
            "birthdate": "",
            "gender": ""
        }

        response = client.post(url, data=data)
        assert response.status_code == 200

        user_after = get_user_by_id(cur, 1)
        assert user_after.username == "Testnavn2"
        assert user_after.email == "email@gmail.com"
        assert user_after.description == "Testdesc"
        assert user_after.birthdate == "i fjor"
        assert user_after.gender == "x"

# Tester krav 1.2.2
def test_successfully_change_password(client: FlaskClient, connect_test_db):
    conn, cur = connect_test_db
    insert_user_info_to_db(conn, cur, "Testnavn", "Testpassord", "epost@gmail.com")
    user_before = get_user_by_id(cur, 1)
    password_before = user_before.password

    with client.application.test_request_context():
        login_user(user_before)

        url = '/change_password'
        data = {
            "old_password": "Testpassord",
            "new_password1": "Testpassord2",
            "new_password2": "Testpassord2",
        }

        response = client.post(url, data=data)

        assert response.status_code == 200
        user_after = get_user_by_id(cur, 1)
        assert password_before != user_after.password
        assert user_after.password == "Testpassord2"
        assert b'passord endret :)' in response.data

# Tester krav 1.2.2
def test_not_inputing_old_password(client: FlaskClient, connect_test_db):
    conn, cur = connect_test_db
    insert_user_info_to_db(conn, cur, "Testnavn", "Testpassord", "epost@gmail.com")
    user_before = get_user_by_id(cur, 1)

    with client.application.test_request_context():
        login_user(user_before)

        url = '/change_password'
        data = {
            "old_password": "",
            "new_password1": "Testpassord2",
            "new_password2": "Testpassord2",
        }

        response = client.post(url, data=data)
        assert response.status_code == 200
        assert b'Vennligst skriv inn det gamle passordet!' in response.data

# Tester krav 1.2.2
def test_not_inputing_new1_password(client: FlaskClient, connect_test_db):
    conn, cur = connect_test_db
    insert_user_info_to_db(conn, cur, "Testnavn", "Testpassord", "epost@gmail.com")
    user_before = get_user_by_id(cur, 1)

    with client.application.test_request_context():
        login_user(user_before)

        url = '/change_password'
        data = {
            "old_password": "Testpassord",
            "new_password1": "",
            "new_password2": "Testpassord2",
        }

        response = client.post(url, data=data)
        assert response.status_code == 200
        assert b'Vennligst skriv inn det nye passordet!' in response.data

# Tester krav 1.2.2
def test_not_inputing_new2_password(client: FlaskClient, connect_test_db):
    conn, cur = connect_test_db
    insert_user_info_to_db(conn, cur, "Testnavn", "Testpassord", "epost@gmail.com")
    user_before = get_user_by_id(cur, 1)

    with client.application.test_request_context():
        login_user(user_before)

        url = '/change_password'
        data = {
            "old_password": "Testpassord",
            "new_password1": "Testpassord2",
            "new_password2": "",
        }

        response = client.post(url, data=data)
        assert response.status_code == 200
        assert b'Vennligst gjenta det nye passordet!' in response.data

# Tester krav 1.2.2
def test_the_new_passwords_dont_match(client: FlaskClient, connect_test_db):
    conn, cur = connect_test_db
    insert_user_info_to_db(conn, cur, "Testnavn", "Testpassord", "epost@gmail.com")
    user_before = get_user_by_id(cur, 1)

    with client.application.test_request_context():
        login_user(user_before)

        url = '/change_password'
        data = {
            "old_password": "Testpassord",
            "new_password1": "Testpassord2",
            "new_password2": "Testpassord3",
        }

        response = client.post(url, data=data)
        assert response.status_code == 200
        assert b'Det nye passordet matcher ikke hverandre' in response.data

# Tester krav 1.2.2
def test_the_old_password_input_doesnt_match_with_password_from_database(client: FlaskClient, connect_test_db):
    conn, cur = connect_test_db
    insert_user_info_to_db(conn, cur, "Testnavn", "Testpassord", "epost@gmail.com")
    user_before = get_user_by_id(cur, 1)

    with client.application.test_request_context():
        login_user(user_before)

        url = '/change_password'
        data = {
            "old_password": "Testpassord34",
            "new_password1": "Testpassord2",
            "new_password2": "Testpassord2",
        }

        response = client.post(url, data=data)
        assert response.status_code == 200
        assert b'Du har skrevet inn feil gammelt passord' in response.data

# Tester krav 1.2.2, og 11.1.2
def test_the_new_password_is_not_validated(client: FlaskClient, connect_test_db):
    conn, cur = connect_test_db
    insert_user_info_to_db(conn, cur, "Testnavn", "Testpassord", "epost@gmail.com")
    user_before = get_user_by_id(cur, 1)

    with client.application.test_request_context():
        login_user(user_before)

        url = '/change_password'
        data = {
            "old_password": "Testpassord34",
            "new_password1": "Tes",
            "new_password2": "Tes",
        }

        response = client.post(url, data=data)
        assert response.status_code == 200
        assert b'Vennligst skriv inn ett passord som er lengre enn 4 tegn' in response.data