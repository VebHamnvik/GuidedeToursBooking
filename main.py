from application.model.database import (
    create_connection,
    create_tables,
    connect_to_db,
    close_connection,
)
from application.model.dbtour import add_tour_to_list_from_db
from application.model.dbbooking import update_list_of_bookings
from application import create_app


if __name__ == "__main__":
    app = create_app()
    conn = create_connection(app.config["DATABASE_URI"])
    create_tables(conn)
    conn, cur = connect_to_db(app)
    add_tour_to_list_from_db(cur)
    update_list_of_bookings(cur)
    close_connection(conn)
    app.run(debug=True)
