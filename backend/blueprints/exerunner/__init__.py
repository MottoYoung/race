from flask import Blueprint

bp = Blueprint('exerunner', __name__, url_prefix='/api/run-exe')

from . import routes
