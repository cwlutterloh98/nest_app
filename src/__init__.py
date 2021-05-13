# imports for Flask
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from .init_db import get_engine, get_connection, create_table, insert_default
# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

def create_app():
    create_table()
    app = Flask(__name__)
    # secret key is used to keep the client side sessions secure
    app.config['SECRET_KEY'] = ' 3d6f45a5fc12445dbac2f59c3b6c7cb1 '

    # hard codded data base credentials! user: root pass: root
    connection = get_connection()
    app.config['SQLALCHEMY_DATABASE_URI'] = connection
    app.config["SQLALCHEMY_ECHO"] = True

    # start FLASK APP
    db.init_app(app)

    # keeps things within the context of the app
    with app.app_context():
        # loginmanager function contains the code that lets your application and flask-login work together
        login_manager = LoginManager()
        login_manager.login_view = 'auth.signIn'
        login_manager.init_app(app)

        # user model contains id,username,password
        from .models import Users

        @login_manager.user_loader
        def load_user(user_id):
            # since the user_id is just the primary key of our user table, use it in the query f
            return Users.query.get(int(user_id))

        # blueprint for auth, main, nest, and dashboard in our app
        from .auth import auth as auth_blueprint
        app.register_blueprint(auth_blueprint)
        from .main import main as main_blueprint
        app.register_blueprint(main_blueprint)
        from .nest_data import nest_data as nest_blueprint
        app.register_blueprint(nest_blueprint)
        from .dashboard import dashboards as dashboard_blueprint
        app.register_blueprint(dashboard_blueprint)

        return app
