import os
import sqlite3
from sqlite3 import Error

# Disse klassene blir testet gjennom create_app funksjonen i test_helpfunctions
class Config:
    DATABASE_URI = "application/final_database.db"
    DEBUG = False


class ProductionConfig(Config):
    DATABASE_URI = "application/final_database.db"


class TestingConfig(Config):
    DATABASE_URI = "test_db.db"


if os.getenv('FLASK_ENV') == 'production':
    app_config = ProductionConfig()
elif os.getenv('FLASK_ENV') == 'testing':
    app_config = TestingConfig()
else:
    app_config = Config()


def create_connection(db_file):
    conn = None

    try:
        conn = sqlite3.connect(db_file, check_same_thread=False)

    except Error as e:
        print(e)

    return conn


def close_connection(conn):
    conn.close()

    return conn


# Lager en funksjon for å opprette tabeller i databasen
def create_tables(conn):
    try:
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
    except Error as e:
        print(e)

def connect_to_db(app):
    database = app.config['DATABASE_URI']
    conn = create_connection(database)
    cur = conn.cursor()

    return conn, cur


def drop_tables(conn):
    cur = conn.cursor()

    drop_users_table = "DROP TABLE IF EXISTS users;"
    drop_tours_table = "DROP TABLE IF EXISTS tours;"
    drop_booking_table = "DROP TABLE IF EXISTS booking;"

    try:
        cur.execute(drop_users_table)
        cur.execute(drop_tours_table)
        cur.execute(drop_booking_table)
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()




