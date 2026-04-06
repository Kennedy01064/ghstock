from app import create_app
from app.extensions import db
from app.models import User

app = create_app()

with app.app_context():
    def upsert_user(username, name, role, password):
        user = User.query.filter_by(username=username).first()
        if not user:
            user = User(username=username, name=name, role=role)
            user.set_password(password)
            db.session.add(user)
            print(f"Created {username} as {role}")
        else:
            user.role = role
            user.set_password(password)
            user.name = name
            print(f"Updated {username} as {role}")
        db.session.commit()

    upsert_user('krojas', 'Kennedy Rojas', 'superadmin', 'krojas')
    upsert_user('eguzman', 'E Guzman', 'admin', 'eguzman')
    upsert_user('dhernandez', 'D Hernandez', 'admin', 'dhernandez')

print("All users have been inserted/updated successfully.")
