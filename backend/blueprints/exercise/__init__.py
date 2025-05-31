from flask import Blueprint

bp = Blueprint('exercise', __name__, url_prefix='/api/exercise')

from . import routes
