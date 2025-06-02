import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    # Replace with your MySQL connection string
    # Example: SQLALCHEMY_DATABASE_URI = 'mysql+mysqlclient://user:password@host/dbname'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or         'mysql+mysqlclient://your_mysql_user:your_mysql_password@localhost/your_mysql_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:' # Use in-memory SQLite for tests
    WTF_CSRF_ENABLED = False # Disable CSRF for simpler form testing
    LOGIN_DISABLED = False # Ensure login is not globally disabled for auth tests
