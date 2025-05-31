from flask import Blueprint

bp = Blueprint('videomaker', __name__, url_prefix='/api/videomaker')

from . import routes
