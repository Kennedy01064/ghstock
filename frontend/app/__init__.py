from flask import Flask
from config import Config
from app.extensions import db, login_manager
from app.models import User

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Flask-Login user loader callback
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    from app.blueprints.auth import auth_bp
    from app.blueprints.dashboard import dashboard_bp
    from app.blueprints.catalog import catalog_bp
    from app.blueprints.orders import orders_bp
    from app.blueprints.dispatch import dispatch_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(catalog_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(dispatch_bp)

    # Create tables (for development)
    with app.app_context():
        db.create_all()

    return app
