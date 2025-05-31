from flask import Blueprint

bp = Blueprint('picturegenerater', __name__, url_prefix='/api/picturegenerater')

from . import routes
