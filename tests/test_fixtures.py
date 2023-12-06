import pytest
import sqlite3


from application.model.tour import Tour
from application.model.user import User

'''Kilde for fixtures mtp database:
https://chat.openai.com/c/5c79aef9-d8d6-4907-9839-7b5f46b93fb3
'''


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():

    conn = sqlite3.connect(r"test_db.db", check_same_thread=False)

    cur = conn.cursor()
    sql_create_users_table = """ CREATE TABLE IF NOT EXISTS users (
                                            id integer PRIMARY KEY,
                                            username text NOT NULL,
                                            password text NOT NULL,
                                            email text NOT NULL,
                                            description text,
                                            birthdate text,
                                            gender text,
                                            image blob

                                        ); """

    sql_create_tour_table = """ CREATE TABLE IF NOT EXISTS tours (
                                            id integer PRIMARY KEY,
                                            title text NOT NULL,
                                            max_capacity int NOT NULL,
                                            description text NOT NULL,
                                            location text NOT NULL,
                                            date text NOT NULL,
                                            price int NOT NULL,
                                            created_by text,
                                            is_active bool, 
                                            image blob 
                                        ); """

    sql_create_bookings_table = """ CREATE TABLE IF NOT EXISTS booking (
                                            id integer PRIMARY KEY,
                                            id_user text NOT NULL,
                                            id_tour text NOT NULL,
                                            participants int NOT NULL,
                                            is_active bool NOT NULL
                                        ); """

    cur.execute(sql_create_users_table)
    cur.execute(sql_create_tour_table)
    cur.execute(sql_create_bookings_table)
    conn.commit()

    yield conn, cur

    conn.close()

@pytest.fixture(autouse=True)
def cleanup_test_database(setup_test_database):
    conn, cur = setup_test_database

    cur.execute("DELETE FROM users")
    cur.execute("DELETE FROM tours")
    cur.execute("DELETE FROM booking")
    conn.commit()

@pytest.fixture()
def connect_test_db():
    conn = sqlite3.connect(r"test_db.db", check_same_thread=False)
    cur = conn.cursor()

    yield conn, cur

    cur.close()
    conn.close()

@pytest.fixture()
def example_tour_1():
    tour = Tour(
        1,
        "Fæsking i Saltstraumen",
        "none",
        200,
        30,
        "Nils-Christian Tjøme",
        "Kveitefiske i Saltstraumen",
        "Saltstraumen",
    )
    return tour


@pytest.fixture()
def example_tour_2():
    tour = Tour(
        2,
        "Fisketur på Tjøme",
        "none",
        200,
        0,
        "Nils-Christian Saltstraum",
        "Vi fisker og drikker også champagne, så samme om vi får noe, vi bestiller kaviar på hytten etterpå",
        "Tjøme",
    )
    return tour


@pytest.fixture()
def example_user_1():
    user = User(1, "sjokoladekake", "1234qwer", "willy@wonka.com")
    return user


@pytest.fixture()
def example_user_2():
    user = User(2, "eplejuice", "qwer1234", "eplejuice@tree.com")
    return user


@pytest.fixture()
def example_user_4():
    user = User(4, "example1", "passwordword", "iexist@notrly.com")
    return user


@pytest.fixture()
def example_user_5():
    user = User(5, "example1", "passwordword", "iexist@notrly.com")
    return user
