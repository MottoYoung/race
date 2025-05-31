from flask import Blueprint

bp = Blueprint('jiaoan', __name__, url_prefix='/api/jiaoan')

from . import routes
