from flask import Blueprint

bp = Blueprint('login', __name__, url_prefix='/api/auth')

from . import routes
