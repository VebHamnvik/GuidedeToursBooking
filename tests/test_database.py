from application import create_app
from application.model.database import create_connection, close_connection, create_tables, drop_tables, connect_to_db
from test_fixtures import connect_test_db

# Tester krav 7.4.1
def test_connection_is_made_to_a_database_through_create_connection():
    conn = create_connection("test_db.db")

    assert conn is not None

    close_connection(conn)

# Tester krav 7.4.1
def test_connection_to_db_is_closed_after_use():
    conn = create_connection("test_db.db")
    assert conn is not None

    close_connection(conn)

    try:
        conn.execute("SELECT 1")
        connection_closed = False
    except Exception as e:
        connection_closed = True

    assert connection_closed

# Tester krav 7.4.1
def test_creation_of_tables_are_successful():
    conn = create_connection("test_db.db")

    assert conn is not None

    cur = conn.cursor()

    create_tables(conn)

    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    users_table_exists = cur.fetchone() is not None

    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tours'")
    tours_table_exists = cur.fetchone() is not None

    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='booking'")
    booking_table_exists = cur.fetchone() is not None

    close_connection(conn)

    assert users_table_exists is True
    assert tours_table_exists is True
    assert booking_table_exists is True

# Tester krav 7.4.1
def test_dropping_tables_after_creation():
    conn = create_connection("test_db.db")

    assert conn is not None

    cur = conn.cursor()
    create_tables(conn)

    drop_tables(conn)

    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    users_table_exists = cur.fetchone() is None

    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tours'")
    tours_table_exists = cur.fetchone() is None

    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='booking'")
    booking_table_exists = cur.fetchone() is None

    close_connection(conn)

    assert users_table_exists is True
    assert tours_table_exists is True
    assert booking_table_exists is True

# Tester krav 7.4.1
def test_connect_to_db():
    app = create_app(config_name='testing')
    database = app.config['DATABASE_URI']

    conn, cur = connect_to_db(app)

    assert conn is not None
    assert cur is not None
    assert database == 'test_db.db'














