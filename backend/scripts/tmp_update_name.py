from app import create_app
from app.extensions import db
from app.models import User

app = create_app()
with app.app_context():
    u = User.query.filter_by(username='krojas').first()
    if u:
        u.name = 'Kennedy'
        db.session.commit()
        print("Updated user name to Kennedy")
    else:
        print("User not found")
