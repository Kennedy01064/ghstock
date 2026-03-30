from flask import Blueprint

dispatch_bp = Blueprint('dispatch', __name__, url_prefix='/dispatch')

from app.blueprints.dispatch import routes
