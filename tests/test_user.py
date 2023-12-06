from application.model.dbuser import insert_user_info_to_db, get_user_by_id
from application.model.dbtour import insert_tour_to_db
from application.model.tour import Tour, list_of_tours
from application.model.user import User, get_tours_from_specific_user
from test_fixtures import connect_test_db, example_user_1, example_user_2, example_user_4, example_user_5, example_tour_1, example_tour_2, setup_test_database, cleanup_test_database



# Tester krav 1.1
def test_user_object_is_correctly_made():
    user = User(1, "Testnavn", "Testpassord", "Testemail")

    assert user.id == 1
    assert user.username == "Testnavn"
    assert user.password == "Testpassord"
    assert user.email == "Testemail"

# Tester krav 1.1, 1.3.1, 1.3.2, 1.3.4
def test_user_object_can_be_made_with_additional_info():
    user = User(1, "Testnavn", "Testpassord", "Testemail", "Testdesc", "Testage", "Testgender")

    assert user.id == 1
    assert user.username == "Testnavn"
    assert user.password == "Testpassord"
    assert user.email == "Testemail"
    assert user.description == "Testdesc"
    assert user.birthdate == "Testage"
    assert user.gender == "Testgender"


def test_checking_if_user_is_added_to_list(example_user_1):
    resultat = example_user_1.check_username_in_list("sjokoladekake")
    assert resultat == True


def test_checking_if_non_unique_username_gets_added(example_user_1):
    duplicate_name = example_user_1.username
    user3 = User(3, duplicate_name, "passord", "sjokissbolle@fakename.com")
    assert user3.username == duplicate_name


def test_checking_if_user_not_in_list(example_user_1):
    resultat = example_user_1.check_username_in_list("sjokolade")
    assert not resultat == True


def test_adding_more_info_to_userprofile(example_user_2):
    example_user_2.add_info(
        "Jeg elsker å gå tur", "02/06/1995", "Male", "string-of-url"
    )
    gender_check = example_user_2.gender
    assert gender_check == "Male"


def test_user_id_is_not_same(example_user_4, example_user_5):
    id_1 = example_user_4.id
    id_2 = example_user_5.id
    assert not id_1 == id_2, f"\nIDs are the same"

# Tester krav 1.3.1, 1.3.2, 1.3.4
def test_adding_tour_to_list_of_created_tours(example_user_1, example_tour_1):
    example_user_1.add_tour_to_list(example_tour_1)
    list = example_user_1.get_list_of_created_tours()

    assert len(list) == 1
    assert example_tour_1 in list
#change password

# Tester krav 2.1.1
def test_adding_multiple_tours_to_list_of_created_tours(example_user_1, example_tour_1, example_tour_2):
    example_user_1.add_tour_to_list(example_tour_1)
    example_user_1.add_tour_to_list(example_tour_2)

    list = example_user_1.get_list_of_created_tours()

    assert len(list) == 2
    assert example_tour_1 in list
    assert example_tour_2 in list

# Tester krav 1.1
def test_get_id(example_user_1):
    id = example_user_1.get_id()
    assert id == '1'

# Tester krav 1.1
def test_get_id_with_multiple_users(example_user_1, example_user_2):
    id1 = example_user_1.get_id()
    id2 = example_user_2.get_id()

    assert id1 != id2
    assert id1 == '1'
    assert id2 == '2'

# Tester krav 1.3.1, 1.3.2, 1.3.4
def test_update_user_info_with_all_inputs(example_user_1, connect_test_db):
    conn, cur = connect_test_db
    old_username = example_user_1.username
    example_user_1.update_user_info(conn, cur, "NewUsername", "NewEmail", "NewDesc", "NewAge", "NewGender")

    assert example_user_1.username == "NewUsername"
    assert example_user_1.username != old_username
    assert example_user_1.description == "NewDesc"

# Tester krav 1.3.1, 1.3.2, 1.3.4
def test_update_user_info_with_some_input(connect_test_db, example_user_1):
    conn, cur = connect_test_db
    old_username = example_user_1.username
    example_user_1.update_user_info(conn, cur, "", "NewEmail", "NewDesc", "NewAge", "NewGender")

    assert example_user_1.username == old_username
    assert example_user_1.email == "NewEmail"

# Tester krav 1.3.1, 1.3.2, 1.3.4
def test_info_stays_the_same_if_no_input(connect_test_db, example_user_1):
    conn, cur = connect_test_db
    old_username = example_user_1.username
    old_desc = example_user_1.description

    example_user_1.update_user_info(conn, cur, "", "", "", "", "")

    assert example_user_1.username == old_username
    assert example_user_1.description == old_desc

# Tester krav 1.3.4
def test_update_user_value_in_db(connect_test_db):
    conn, cur = connect_test_db
    insert_user_info_to_db(conn, cur, "Testnavn", "Testpassord", "Testemail")
    user = get_user_by_id(cur, 1)
    old_email = user.email

    user.update_user_value_in_db(conn, cur, "email", "Newemail")
    updated_user = get_user_by_id(cur, 1)

    assert updated_user.email == "Newemail"
    assert updated_user.email != old_email

# Tester krav 2.1.1
def test_get_tours_from_specific_user(connect_test_db):
    conn, cur = connect_test_db
    insert_user_info_to_db(conn, cur, "Testnavn", "Testpassord", "Testemail")
    insert_tour_to_db(conn, cur, "Title1", 10, "Desc1", "Loc1", "Date1", 100, 1)
    insert_tour_to_db(conn, cur, "Title2", 20, "Desc2", "Loc2", "Date2", 200, 1)

    user = get_user_by_id(cur, 1)

    list_of_created_tours = get_tours_from_specific_user(cur, 1)

    assert len(list_of_created_tours) == 2
    assert list_of_created_tours[0]['title'] == "Title1"
    assert list_of_created_tours[1]['title'] == "Title2"

# Tester krav 2.1.1
def test_get_tours_from_specific_user_when_no_tours(connect_test_db):
    conn, cur = connect_test_db
    insert_user_info_to_db(conn, cur, "Testnavn", "Testpassord", "Testmail")


    user = get_user_by_id(cur, 1)
    list_of_created_tours = get_tours_from_specific_user(cur, 1)

    assert len(list_of_created_tours) == 0



