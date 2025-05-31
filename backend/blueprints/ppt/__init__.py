from flask import Blueprint

bp = Blueprint('ppt', __name__, url_prefix='/api/ppt')

from . import routes
