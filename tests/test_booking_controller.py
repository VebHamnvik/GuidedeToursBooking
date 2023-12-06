import pytest
from flask.testing import FlaskClient
from flask_login import login_user, logout_user

from application import create_app
from application.model.database import create_connection, create_tables, connect_to_db, drop_tables
from application.model.dbtour import get_tour_by_id, insert_tour_to_db
from application.model.dbbooking import get_rows_bookings, create_booking, find_info_about_tours_user_has_booked
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

# Tester krav 3.2
def test_if_logged_in_user_can_get_to_my_bookings(client: FlaskClient):
    user = User(1, "Testnavn", "Testpassord", "email@gmail.com")

    with client.application.test_request_context():
        login_user(user)

        response = client.get('/my_bookings')

        assert response.status_code == 200
        assert b'Her er en liste over dine bookinger:' in response.data

        logout_user()

def test_not_logged_in_user_cant_get_to_my_bookings(client: FlaskClient):
    with client:
        response = client.get('/my_bookings')

        assert response.status_code == 401
        assert b'Authentication required for this API endpoint' in response.data

# Tester krav 3.1.1
def test_if_logged_in_user_can_get_to_book_this_tour(client: FlaskClient, connect_test_db):
    conn, cur = connect_test_db
    insert_tour_to_db(conn, cur, "Dette er tittel", 10, "Desc", "Location", "Date", 1000, 1)
    tour = get_tour_by_id(cur, 1)
    tour.add_tour_to_list_of_tours(cur)
    user = User(1, "Testnavn", "Testpassord", "email@gmail.com")

    with client.application.test_request_context():
        login_user(user)
        response = client.get('/book_this_tour/1')

        assert response.status_code == 200
        assert b'Hvor mange er dere?' in response.data
        assert b'Book denne touren' in response.data

        logout_user()

def test_not_logged_in_user_cant_get_to_book_this_tour(client: FlaskClient, connect_test_db):
    conn, cur = connect_test_db
    insert_tour_to_db(conn, cur, "Dette er tittel", 10, "Desc", "Location", "Date", 1000, 1)
    tour = get_tour_by_id(cur, 1)
    tour.add_tour_to_list_of_tours(cur)
    with client:
        response = client.get('/book_this_tour/1')

        assert response.status_code == 401
        assert b'Authentication required for this API endpoint' in response.data

# Tester krav 3.1.1 og 9.1.3
def test_logged_in_user_can_book_this_tour(client: FlaskClient, connect_test_db):
    conn, cur = connect_test_db
    insert_tour_to_db(conn, cur, "Dette er tittel", 10, "Desc", "Location", "Date", 1000, 1)
    tour = get_tour_by_id(cur, 1)
    tour.add_tour_to_list_of_tours(cur)
    user = User(1, "Testnavn", "Testpassord", "email@gmail.com")
    number_of_bookings = get_rows_bookings(cur)

    with client.application.test_request_context():
        login_user(user)
        response = client.get('/book_this_tour/1')

        assert response.status_code == 200
        assert b'Hvor mange er dere?' in response.data
        assert b'Book denne touren' in response.data

        data = {
            'participants': '1'
        }
        form_data = "&".join([f"{key}={value}" for key, value in data.items()])
        test_booking = client.post('/book_this_tour/1', data=form_data, content_type='application/x-www-form-urlencoded')

        assert test_booking.status_code == 302
        assert get_rows_bookings(cur) == 1
        assert get_rows_bookings(cur) != number_of_bookings

        logout_user()

# Tester krav 3.1.1
def test_logged_in_user_gets_flashed_if_trying_to_book_more_than_max_capacity_of_tour(client: FlaskClient, connect_test_db):
    conn, cur = connect_test_db
    insert_tour_to_db(conn, cur, "Dette er tittel", 4, "Desc", "Location", "Date", 1000, 1)
    tour = get_tour_by_id(cur, 1)
    tour.add_tour_to_list_of_tours(cur)
    user = User(1, "Testnavn", "Testpassord", "email@gmail.com")

    with client.application.test_request_context():
        login_user(user)
        response = client.get('/book_this_tour/1')

        assert response.status_code == 200
        assert b'Hvor mange er dere?' in response.data
        assert b'Book denne touren' in response.data

        data = {
            'participants': '5'
        }
        form_data = "&".join([f"{key}={value}" for key, value in data.items()])
        test_booking = client.post('/book_this_tour/1', data=form_data, content_type='application/x-www-form-urlencoded')

        assert test_booking.status_code == 200
        assert b'Beklager, det er ikke plass til' in test_booking.data

        logout_user()

# Tester krav 3.1.1
def test_logged_in_user_gets_flashed_if_trying_to_book_less_than_one_participant(client: FlaskClient, connect_test_db):
    conn, cur = connect_test_db
    insert_tour_to_db(conn, cur, "Dette er tittel", 4, "Desc", "Location", "Date", 1000, 1)
    tour = get_tour_by_id(cur, 1)
    tour.add_tour_to_list_of_tours(cur)
    user = User(1, "Testnavn", "Testpassord", "email@gmail.com")

    with client.application.test_request_context():
        login_user(user)
        response = client.get('/book_this_tour/1')

        assert response.status_code == 200
        assert b'Hvor mange er dere?' in response.data
        assert b'Book denne touren' in response.data

        data = {
            'participants': '0'
        }
        form_data = "&".join([f"{key}={value}" for key, value in data.items()])
        test_booking = client.post('/book_this_tour/1', data=form_data, content_type='application/x-www-form-urlencoded')

        assert test_booking.status_code == 200
        assert b'Du kan ikke booke for mindre enn 1 person :/' in test_booking.data

        logout_user()

# Tester krav 3.1.1 og 9.1.3
def test_if_booking_is_not_made_correctly_it_is_not_inserted_into_the_database(client: FlaskClient, connect_test_db):
    conn, cur = connect_test_db
    insert_tour_to_db(conn, cur, "Dette er tittel", 1, "Desc", "Location", "Date", 1000, 1)
    tour = get_tour_by_id(cur, 1)
    tour.add_tour_to_list_of_tours(cur)
    user = User(1, "Testnavn", "Testpassord", "email@gmail.com")
    number_of_bookings = get_rows_bookings(cur)

    with client.application.test_request_context():
        login_user(user)
        response = client.get('/book_this_tour/1')

        assert response.status_code == 200
        assert b'Hvor mange er dere?' in response.data
        assert b'Book denne touren' in response.data

        data = {
            'participants': '2'
        }
        form_data = "&".join([f"{key}={value}" for key, value in data.items()])
        test_booking = client.post('/book_this_tour/1', data=form_data, content_type='application/x-www-form-urlencoded')

        assert test_booking.status_code == 200
        assert get_rows_bookings(cur) == 0
        assert b'Beklager, det er ikke plass til' in test_booking.data
        assert get_rows_bookings(cur) == number_of_bookings

        logout_user()

def test_not_logged_in_users_cant_get_to_fake_payment(client: FlaskClient):
    with client.application.test_request_context():
        response = client.get('/fake_payment')

        assert response.status_code == 401

def test_logged_in_users_can_get_to_fake_payment(client: FlaskClient):
    user = User(1, "Testnavn", "Testpassord", "email@gmail.com")

    with client.application.test_request_context():
        login_user(user)

        response = client.get('/fake_payment')

        assert response.status_code == 200
        assert b'betalingsmetode' in response.data

        logout_user()

# Tester krav 3.1.4
def test_logged_in_user_can_cancel_their_booking(client: FlaskClient, connect_test_db):
    conn, cur = connect_test_db
    insert_tour_to_db(conn, cur, "Dette er tittel", 10, "Desc", "Location", "Date", 1000, 1)
    tour = get_tour_by_id(cur, 1)
    tour.add_tour_to_list_of_tours(cur)
    user = User(1, "Testnavn", "Testpassord", "email@gmail.com")
    create_booking(conn, cur, 1, 1, 4)
    number_of_bookings = get_rows_bookings(cur)
    number_of_bookings_before_cancel = find_info_about_tours_user_has_booked(cur, 1)

    assert number_of_bookings == 1

    with client.application.test_request_context():
        login_user(user)
        url = '/cancel_booking'
        data = {
            "id_tour": "1",
            "id_user": "1",
        }
        form_data = "&".join([f"{key}={value}" for key, value in data.items()])
        response = client.post(url, data=form_data, content_type='application/x-www-form-urlencoded')

        number_of_bookings_after_cancel = find_info_about_tours_user_has_booked(cur, 1)

        assert len(number_of_bookings_after_cancel) == 0
        assert len(number_of_bookings_before_cancel) > len(number_of_bookings_after_cancel)
        assert len(number_of_bookings_after_cancel) == len(number_of_bookings_before_cancel) - 1






