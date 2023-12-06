import pytest
from flask.testing import FlaskClient
from flask_login import login_user, logout_user

from application import create_app
from application.model.database import create_connection, create_tables, connect_to_db, drop_tables
from application.model.dbtour import get_tour_by_id, insert_tour_to_db, get_rows_tours
from application.model.user import User
from application.model.tour import list_of_tours
from test_fixtures import connect_test_db

@pytest.fixture
def app():
    app = create_app(config_name='testing')
    app.config['TESTING'] = True
    app.config['DEBUG'] = True
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

# Tester krav 2.1.1
def test_if_logged_in_user_can_get_to_my_tours(client: FlaskClient):
    user = User(1, "Testnavn", "Testpassord", "email@gmail.com")

    with client.application.test_request_context():
        login_user(user)
        response = client.get('/my_tours')

        assert response.status_code == 200
        assert b'Her er en liste over dine annonser:' in response.data

        logout_user()

def test_not_logged_in_user_cant_get_to_my_tours(client: FlaskClient):
    with client:
        response = client.get('/my_tours')

        assert response.status_code == 401
        assert b'Authentication required for this API endpoint' in response.data


def test_not_logged_in_user_cant_get_to_create_tour(client: FlaskClient):
    with client:
        response = client.get('/create_tour')

        assert response.status_code == 401
        assert b'Authentication required for this API endpoint' in response.data

# Tester krav 2.1
def test_logged_in_users_can_get_to_create_tour(client: FlaskClient):
    user = User(1, "Testnavn", "Testpassord", "email@gmail.com")

    with client.application.test_request_context():
        login_user(user)

        response = client.get('/create_tour')

        assert response.status_code == 200
        assert b'Lag en annonse!' in response.data

        logout_user()

# Tester krav 2.1
def test_a_logged_in_user_can_create_a_tour(client: FlaskClient):
    user = User(1, "Testnavn", "Testpassord", "email@gmail.com")

    with client.application.test_request_context():
        login_user(user)

        url = '/create_tour'
        data = {
            "title": "Testtittel",
            "max_capacity": 54,
            "description": "Testdesc",
            "location": "Testlocation",
            "date": "Testdate",
            "price": 100,
        }
        response = client.post(url, data=data)

        assert response.status_code == 302
        assert response.location == '/my_tours'

        logout_user()

# Tester krav 2.1 og 9.1.2
def test_verify_made_tour_is_inserted_into_database(client: FlaskClient, connect_test_db):
    conn, cur = connect_test_db
    user = User(1, "Testnavn", "Testpassord", "email@gmail.com")

    with client.application.test_request_context():
        login_user(user)

        url = '/create_tour'
        data = {
            "title": "Testtittel",
            "max_capacity": 54,
            "description": "Testdesc",
            "location": "Testlocation",
            "date": "Testdate",
            "price": 100,
        }
        response = client.post(url, data=data)
        tour = get_tour_by_id(cur, 1)

        assert tour.title == "Testtittel"
        assert tour.description == "Testdesc"
        assert tour.price == 100

        logout_user()

# Tester krav 2.1
def test_flash_correctly_when_title_not_input_in_create_tour(client: FlaskClient):
    user = User(1, "Testnavn", "Testpassord", "email@gmail.com")

    with client.application.test_request_context():
        login_user(user)

        url = '/create_tour'
        data = {
            "title": "",
            "max_capacity": 54,
            "description": "Testdesc",
            "location": "Testlocation",
            "date": "Testdate",
            "price": 100,
        }
        response = client.post(url, data=data)

        assert response.status_code == 200
        assert b'Vennligst skriv inn tittel!' in response.data

        logout_user()

# Tester krav 2.1
def test_flash_correctly_when_max_capacity_not_input_in_create_tour(client: FlaskClient):
    user = User(1, "Testnavn", "Testpassord", "email@gmail.com")

    with client.application.test_request_context():
        login_user(user)

        url = '/create_tour'
        data = {
            "title": "Testtittel",
            "max_capacity": "",
            "description": "Testdesc",
            "location": "Testlocation",
            "date": "Testdate",
            "price": 100,
        }
        response = client.post(url, data=data)

        assert response.status_code == 200
        assert b'Vennligst skriv inn kapasitet!' in response.data

        logout_user()

# Tester krav 2.1
def test_flash_correctly_when_description_not_input_in_create_tour(client: FlaskClient):
    user = User(1, "Testnavn", "Testpassord", "email@gmail.com")

    with client.application.test_request_context():
        login_user(user)

        url = '/create_tour'
        data = {
            "title": "Testtittel",
            "max_capacity": 100,
            "description": "",
            "location": "Testlocation",
            "date": "Testdate",
            "price": 100,
        }
        response = client.post(url, data=data)

        assert response.status_code == 200
        assert b'Vennligst skriv inn beskrivelse!' in response.data

        logout_user()

# Tester krav 2.1
def test_flash_correctly_when_location_not_input_in_create_tour(client: FlaskClient):
    user = User(1, "Testnavn", "Testpassord", "email@gmail.com")

    with client.application.test_request_context():
        login_user(user)

        url = '/create_tour'
        data = {
            "title": "Testtittel",
            "max_capacity": 100,
            "description": "Testdesc",
            "location": "",
            "date": "Testdate",
            "price": 100,
        }
        response = client.post(url, data=data)

        assert response.status_code == 200
        assert b'Vennligst skriv inn lokasjon!' in response.data

        logout_user()

# Tester krav 2.1
def test_flash_correctly_when_date_not_input_in_create_tour(client: FlaskClient):
    user = User(1, "Testnavn", "Testpassord", "email@gmail.com")

    with client.application.test_request_context():
        login_user(user)

        url = '/create_tour'
        data = {
            "title": "Testtittel",
            "max_capacity": 100,
            "description": "Testdesc",
            "location": "Testlocation",
            "date": "",
            "price": 100,
        }
        response = client.post(url, data=data)

        assert response.status_code == 200
        assert b'Vennligst skriv inn dato!' in response.data

        logout_user()

# Tester krav 2.1
def test_flash_correctly_when_price_not_input_in_create_tour(client: FlaskClient):
    user = User(1, "Testnavn", "Testpassord", "email@gmail.com")

    with client.application.test_request_context():
        login_user(user)

        url = '/create_tour'
        data = {
            "title": "Testtittel",
            "max_capacity": 100,
            "description": "Testdesc",
            "location": "Testlocation",
            "date": "Testdate",
            "price": "",
        }
        response = client.post(url, data=data)

        assert response.status_code == 200
        assert b'Vennligst skriv inn prisen!' in response.data

        logout_user()

# Tester krav 2.1 og 9.1.2
def test_the_new_tour_is_not_added_to_database_if_not_input_is_correct(client: FlaskClient, connect_test_db):
    conn, cur = connect_test_db
    user = User(1, "Testnavn", "Testpassord", "email@gmail.com")

    with client.application.test_request_context():
        login_user(user)

        url = '/create_tour'
        data = {
            "title": "",
            "max_capacity": 54,
            "description": "Testdesc",
            "location": "Testlocation",
            "date": "Testdate",
            "price": 100,
        }
        response = client.post(url, data=data)

        tour = get_tour_by_id(cur, 1)
        assert tour is None

        logout_user()

def test_tour_object_gets_added_to_global_list_after_being_created_through_api(client: FlaskClient):
    user = User(1, "Testnavn", "Testpassord", "email@gmail.com")
    length_list_of_tours = len(list_of_tours)

    with client.application.test_request_context():
        login_user(user)

        url = '/create_tour'
        data = {
            "title": "Testtittel",
            "max_capacity": 54,
            "description": "Testdesc",
            "location": "Testlocation",
            "date": "Testdate",
            "price": 100,
        }
        response = client.post(url, data=data)
        assert len(list_of_tours) == length_list_of_tours+1

        logout_user()

def test_tour_object_gets_added_to_user_list_after_being_created_through_api(client: FlaskClient):
    user = User(1, "Testnavn", "Testpassord", "email@gmail.com")
    length_of_list_of_created_tours = len(user.list_of_created_tours)
    with client.application.test_request_context():
        login_user(user)

        url = '/create_tour'
        data = {
            "title": "Testtittel",
            "max_capacity": 54,
            "description": "Testdesc",
            "location": "Testlocation",
            "date": "Testdate",
            "price": 100,
        }
        response = client.post(url, data=data)
        assert len(user.list_of_created_tours) == length_of_list_of_created_tours+1

        logout_user()

# Tester krav 2.5.2
def test_not_logged_in_user_can_get_to_outtour(client: FlaskClient, connect_test_db):
    conn, cur = connect_test_db
    insert_tour_to_db(conn, cur, "Dette er tittel", 10, "Desc", "Location", "Date", 1000, 1)
    tour = get_tour_by_id(cur, 1)
    tour.add_tour_to_list_of_tours(cur)

    with client:
        response = client.get('/notloggedtour/1')

        assert response.status_code == 200
        assert b'Dette er tittel' in response.data

# Tester krav 2.5.2
def test_not_logged_in_user_can_not_get_to_intour(client:FlaskClient, connect_test_db):
    conn, cur = connect_test_db
    insert_tour_to_db(conn, cur, "Dette er tittel", 10, "Desc", "Location", "Date", 1000, 1)
    tour = get_tour_by_id(cur, 1)
    tour.add_tour_to_list_of_tours(cur)

    with client:
        response = client.get('/loggedtour/1')

        assert response.status_code == 401
        assert b'Authentication required for this API endpoint' in response.data

# Tester krav 2.5.2
def test_logged_in_users_can_get_to_intour(client: FlaskClient, connect_test_db):
    conn, cur = connect_test_db
    insert_tour_to_db(conn, cur, "Dette er tittel", 10, "Desc", "Location", "Date", 1000, 1)
    tour = get_tour_by_id(cur, 1)
    tour.add_tour_to_list_of_tours(cur)
    user = User(1, "Username", "Password", "email")

    with client.application.test_request_context():
        login_user(user)
        response = client.get('/loggedtour/1')

        assert response.status_code == 200
        assert b'Dette er tittel' in response.data

        logout_user()

# Tester krav 2.4.4
def test_logged_in_users_can_cancel_their_tour(client: FlaskClient, connect_test_db):
    conn, cur = connect_test_db
    insert_tour_to_db(conn, cur, "Dette er tittel", 10, "Desc", "Location", "Date", 1000, 1)
    tour = get_tour_by_id(cur, 1)
    tour.add_tour_to_list_of_tours(cur)
    user = User(1, "Username", "Password", "Email")

    with client.application.test_request_context():
        login_user(user)
        url = '/cancel_tour'
        data = {
            "id_tour": "1"
        }
        form_data = "&".join([f"{key}={value}" for key, value in data.items()])
        # https://chat.openai.com/share/d352f569-4a19-4c7c-a197-27c18107744a

        response = client.post(url, data=form_data, content_type='application/x-www-form-urlencoded')
        deleted_tour = get_tour_by_id(cur, 1)

        assert response.status_code == 302
        assert deleted_tour.is_active == False

        logout_user()

