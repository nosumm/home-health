from flask import Blueprint

bp = Blueprint('about', __name__)

from website.about import routes