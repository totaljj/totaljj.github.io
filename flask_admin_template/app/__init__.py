from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login' # This will be the blueprint name 'auth' and the route name 'login'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db) # Initialize migrate here
    login.init_app(app)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # A simple main blueprint for non-auth parts of the app
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)


    @app.route('/test/') # This is a test route, can be removed later
    def test_page():
        return '<h1>Testing the Flask Application Factory!</h1>'

    return app

# Import models here to make them available for Flask-Migrate
from app import models # Add this line
