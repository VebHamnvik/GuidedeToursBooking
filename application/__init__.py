from flask import Flask, jsonify
from flask_login import LoginManager

def create_app(config_name='production'):
    app = Flask(__name__, template_folder="template")
    app.config['SECRET_KEY'] = 'hemmelignøkkel'

    if config_name == 'production':
        app.config.from_object('application.model.database.ProductionConfig')
    elif config_name == 'testing':
        app.config.from_object('application.model.database.TestingConfig')

    else:
        raise ValueError("Invalid configuration name")

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "login"

    from application.controller.home_controller import home_blueprint
    from application.controller.user_controller import user_blueprint
    from application.controller.tour_controller import tour_blueprint
    from application.controller.booking_controller import booking_blueprint

    app.register_blueprint(home_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(tour_blueprint)
    app.register_blueprint(booking_blueprint)

    from application.model.database import connect_to_db, close_connection
    from application.model.dbuser import get_user_by_id

    @login_manager.user_loader
    def load_user(user_id):
        conn, cur = connect_to_db(app)
        sql = 'SELECT id FROM users WHERE id = ?'
        cur.execute(sql, (user_id,))
        id_row = cur.fetchone()

        if id_row:
            user_id = id_row[0]
            return get_user_by_id(cur, user_id)
        else:
            close_connection(conn)
            return None

    @login_manager.unauthorized_handler
    def unauthorized():
        response = jsonify({
            'error': 'Unauthorized',
            'message': 'Authentication required for this API endpoint'
        })
        response.status_code = 401
        return response

    return app

