from application.controller.user_controller import change_password, registrer_user
from application.controller.tour_controller import create_tour
from application.model.dbtour import insert_tour_to_db, get_tour_by_id, get_rows_tours
from application.model.dbuser import insert_user_info_to_db, get_row_from_users, get_password_from_db, \
    get_username_from_db, get_user_by_id, get_rows_users, get_id_by_username, get_username_by_id
from application.model.user import User
from application.model.tour import Tour
from test_fixtures import setup_test_database, connect_test_db, cleanup_test_database


# Tester krav 9.1.1
def test_inserting_user_into_test_db(connect_test_db):
    conn, cur = connect_test_db
    insert_user_info_to_db(conn, cur, "Testnavn", "Testpassord", "Testemail")

    row = get_row_from_users(cur)

    expected_username = "Testnavn"
    expected_password = "Testpassord"
    expected_email = "Testemail"

    assert row is not None
    assert row[1] == expected_username
    assert row[2] == expected_password
    assert row[3] == expected_email

# Tester krav 9.1.1
def test_get_username_from_db(connect_test_db):
    conn, cur = connect_test_db
    insert_user_info_to_db(conn, cur, "Testnavn", "Testpassord", "Testemail")

    username = get_username_from_db(cur, "Testnavn")

    assert username[0] == "Testnavn"

# Tester krav 9.1.1
def test_get_username_from_db_wrong_username(connect_test_db):
    conn, cur = connect_test_db
    insert_user_info_to_db(conn, cur, "Testnavn", "Testpassord", "Testemail")

    username = get_username_from_db(cur, "FeilNavn")

    assert username is None

# Tester krav 9.1.1
def test_get_user_password_from_db(connect_test_db):
    conn, cur = connect_test_db
    insert_user_info_to_db(conn, cur, "Testnavn", "Testpassord", "Testemail")

    password = get_password_from_db(cur, "Testnavn")

    assert password[0] == "Testpassord"

# Tester krav 9.1.1
def test_get_password_from_db_if_wrong_username(connect_test_db):
    conn, cur = connect_test_db
    insert_user_info_to_db(conn, cur, "Testnavn", "Testpassord", "Testemail")

    password = get_password_from_db(cur, "FeilUsername")

    assert password is None

# Tester krav 9.1.1
def test_get_user_by_id(connect_test_db):
    conn, cur = connect_test_db
    insert_user_info_to_db(conn, cur, "Testnavn", "Testpassord", "Testemail")

    user = get_user_by_id(cur, 1)

    username = user.username
    password = user.password
    email = user.email

    assert username == "Testnavn"
    assert password == "Testpassord"
    assert email == "Testemail"

# Tester krav 9.1.1
def test_get_user_by_id_when_id_not_in_database_should_be_none(connect_test_db):
    conn, cur = connect_test_db
    user = get_user_by_id(cur, 1)

    assert user is None

# Tester krav 9.1.1
def test_get_id_by_username(connect_test_db):
    conn, cur = connect_test_db
    insert_user_info_to_db(conn, cur, "Testnavn", "Testpassord", "Testemail")

    user_id = get_id_by_username(cur, "Testnavn")

    assert user_id == 1

# Tester krav 9.1.1
def test_get_id_by_username_when_multiple_users(connect_test_db):
    conn, cur = connect_test_db
    insert_user_info_to_db(conn, cur, "Testnavn", "Testpassord", "Testemail")
    insert_user_info_to_db(conn, cur, "Testnavn2", "Testpassord2", "Testemail2")
    insert_user_info_to_db(conn, cur, "Testnavn3", "Testpassord3", "Testemail3")
    insert_user_info_to_db(conn, cur, "Testnavn4", "Testpassord4", "Testemail4")

    user_id = get_id_by_username(cur, "Testnavn3")

    assert user_id == 3

# Tester krav 9.1.1
def test_get_id_by_username_when_wrong_username(connect_test_db):
    conn, cur = connect_test_db
    insert_user_info_to_db(conn, cur, "Testnavn", "Testpassord", "Testemail")
    insert_user_info_to_db(conn, cur, "Testnavn2", "Testpassord2", "Testemail2")
    insert_user_info_to_db(conn, cur, "Testnavn3", "Testpassord3", "Testemail3")
    insert_user_info_to_db(conn, cur, "Testnavn4", "Testpassord4", "Testemail4")

    user_id = get_id_by_username(cur, "Testnavn34")

    assert user_id is None


def test_get_correct_number_rows_users(connect_test_db):
    conn, cur = connect_test_db
    insert_user_info_to_db(conn, cur, "Testnavn", "Testpassord", "Testemail")
    insert_user_info_to_db(conn, cur, "Testnavn2", "Testpassord2", "Testemail2")

    rows = get_rows_users(cur)

    assert rows == 2


def test_get_one_row_users(connect_test_db):
    conn, cur = connect_test_db
    insert_user_info_to_db(conn, cur, "Testnavn", "Testpassord", "Testemail")

    rows = get_rows_users(cur)

    assert rows == 1


def test_get_rows_users(connect_test_db):
    conn, cur = connect_test_db
    insert_user_info_to_db(conn, cur, "Testnavn", "Testpassord", "Testemail")
    insert_user_info_to_db(conn, cur, "Testnavn2", "Testpassord2", "Testemail2")
    insert_user_info_to_db(conn, cur, "Testnavn3", "Testpassord3", "Testemail3")
    insert_user_info_to_db(conn, cur, "Testnavn4", "Testpassord4", "Testemail4")

    rows = get_rows_users(cur)

    assert rows != 1


# Tester krav 1.2.2
def test_changing_password_updates_in_db(connect_test_db):
    conn, cur = connect_test_db

    insert_user_info_to_db(conn, cur, "Testnavn", "GammeltPassord", "Testemail")
    user = get_user_by_id(cur, 1)
    new_password = "NyttPassord"
    user.change_password(conn, cur, new_password)

    database_sjekk = get_password_from_db(cur, "Testnavn")
    database_nytt_passord = database_sjekk[0]

    gammelt_passord = "GammeltPassord"

    assert gammelt_passord != new_password
    assert new_password == database_nytt_passord

# Tester krav 1.2.2
def test_new_password_is_not_old_password(connect_test_db):
    conn, cur = connect_test_db

    insert_user_info_to_db(conn, cur, "Testnavn", "GammeltPassord", "Testemail")
    user = get_user_by_id(cur, 1)
    new_password = "NyttPassord"
    user.change_password(conn, cur, new_password)

    updated_password = get_password_from_db(cur, "Testnavn")

    assert "GammeltPassord" != updated_password


# Tester krav 2.1.1
def test_get_tours_from_specific_user1(connect_test_db):
    conn, cur = connect_test_db

    insert_tour_to_db(conn, cur, "Tour 1", 10, "Description 1", "Location 1", "2023-01-01", 50, 1)
    tour_id1 = get_rows_tours(cur)
    tour_1 = Tour(tour_id1, "Tour 1", "2023-01-01", 50, 10, 1, "Description 1", "Location 1")
    insert_tour_to_db(conn, cur, "Tour 2", 10, "Description 2", "Location 2", "2023-01-02", 50, 1)
    tour_id2 = get_rows_tours(cur)
    tour_2 = Tour(tour_id2, "Tour 2", "2023-01-02", 50, 10, 1, "Description 2", "Location 2")
    user = User(id=1, username="Bruker1", password="password", email="test@example.com",
                description="TourGuide", birthdate="11-04-1993", gender="M")

    user.add_tour_to_list(tour_1)
    user.add_tour_to_list(tour_2)

    list_of_created_tours = user.get_list_of_created_tours()

    assert len(list_of_created_tours) == 2

# Tester krav 1.3.1, 1.3.2, 1.3.4
def test_update_the_user_information_in_db(connect_test_db):
    conn, cur = connect_test_db

    insert_user_info_to_db(conn, cur, "Testnavn", "GammeltPassord", "Testemail", "FomerGuide", "12.12.2012", "M")
    user = get_user_by_id(cur, 1)
    user.update_user_info(conn, cur, "new_user", "new@example.com", "NewGuide", "12.12.2012", "M")


    assert user.username == "new_user"
    assert user.birthdate == "12.12.2012"
    assert user.gender == "M"

# Tester krav 9.1.1
def test_get_username_by_id_if_user_exists(connect_test_db):
    conn, cur = connect_test_db
    insert_user_info_to_db(conn, cur, "Testnavn", "GammeltPassord", "Testemail", "FomerGuide", "12.12.2012", "M")
    username = get_username_by_id(cur, (1,))

    assert username is not None
    assert username == "Testnavn"

# Tester krav 9.1.1
def test_get_username_by_id_if_user_doesnt_exists(connect_test_db):
    conn, cur = connect_test_db
    username = get_username_by_id(cur, (1,))

    assert username is None
