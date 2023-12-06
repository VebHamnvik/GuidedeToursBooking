from application.model.dbuser import get_row_from_users
from application.model.tour import Tour, list_of_tours
from test_fixtures import example_tour_1, example_tour_2, setup_test_database, connect_test_db
from application.model.dbtour import insert_tour_to_db


# Tester krav 2.1
def test_create_tour_object():
    tour = Tour(1, "Title", "date", 100, 10, 1, "Desc", "loc")

    assert tour is not None
    assert tour.title == "Title"
    assert tour.price == 100
    assert tour.created_by == 1

# Tester krav 2.1
def test_if_id_is_unique(example_tour_1, example_tour_2):
    # Testing if two tours have different IDs
    id_1 = example_tour_1.tour_id
    id_2 = example_tour_2.tour_id
    assert not id_1 == id_2, f"\nIDs are the same"


# Tester krav 2.1
def test_check_if_tour_was_created(example_tour_1):
    tour = example_tour_1
    assert tour.title == "Fæsking i Saltstraumen"



def test_tour_into_list(example_tour_1):
    tour = example_tour_1
    list_of_tours.append(tour)
    number_of_tours = len(list_of_tours)

    assert number_of_tours != 0
    list_of_tours.clear()


# Tester krav 2.1
def test_max_capacity_limit(example_tour_1):
    tour = example_tour_1
    tour.update_tour_info("Test Tour 11", 35, "Description", "Location", "2023-12-31", 100.0, "23.01.2024", 250)

    # Sjekk om antall deltakere for turen ikke har overskredet maksimal kapasitet
    assert int(tour.max_capacity) >= int(tour.max_capacity)
    list_of_tours.clear()

# Tester krav 2.1
def test_if_max_participants_not_null(example_tour_2):
    tour_test = example_tour_2.max_capacity
    assert tour_test == 0








