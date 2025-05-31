from flask import Blueprint

bp = Blueprint('pptvideo', __name__, 
               url_prefix='/api/pptvideo',
               static_folder='static',
               static_url_path='/static/pptvideo')

from . import routes
