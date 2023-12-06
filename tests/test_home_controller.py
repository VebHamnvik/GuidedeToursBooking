import pytest
from flask.testing import FlaskClient
from flask_login import login_user, logout_user

from application import create_app
from application.model.database import create_connection, create_tables, connect_to_db, drop_tables
from application.model.user import User

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

# Tester krav 2.5.1
def test_home_for_not_logged_in_users(client: FlaskClient):
    with client.application.test_request_context():
        response = client.get('/')

        assert response.status_code == 200
        assert b'Hjem' in response.data
        assert b'Guidede turer' in response.data


# Tester krav 2.5.1
def test_home_for_logged_in_users(client: FlaskClient):
    user = User(1, "Testnavn", "Testpassord", "Epost@gmail.com")

    with client.application.test_request_context():
        login_user(user)

        response = client.get('/')
        assert response.status_code == 200
        assert b'Hjem' in response.data
        assert b'Guidede turer' in response.data

        logout_user()

# Tester krav 1.2.1
def test_dashboard_for_not_logged_in_users(client: FlaskClient):
    with client.application.test_request_context():
        response = client.get('/dashboard')

        assert response.status_code == 401
        assert b'Authentication required for this API endpoint' in response.data

# Tester krav 1.2.1 og 2.5.1
def test_deashboard_for_logged_in_users(client: FlaskClient):
    user = User(1, "Testnavn", "Testpassord", "Epost@gmail.com")
    with client.application.test_request_context():
        login_user(user)
        response = client.get('/dashboard')

        assert response.status_code == 200
        assert b'Hjem' in response.data
        assert b'Mine annonser' in response.data
        assert b'Mine bookinger' in response.data
        assert b'Min profil' in response.data

        logout_user()