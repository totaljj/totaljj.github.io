from flask import Blueprint

bp = Blueprint('main', __name__, template_folder='templates')

from app.main import routes # Import routes after bp is created
