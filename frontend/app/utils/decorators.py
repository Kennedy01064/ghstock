from functools import wraps
from flask import abort, session
from flask_login import current_user, login_required

def superadmin_required(f):
    """Decorator that requires the user to be logged in AND have the 'superadmin' role."""
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'superadmin' or session.get('view_as_admin'):
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

def management_required(f):
    """Decorator that requires the user to be logged in AND have 'manager' or 'superadmin' role."""
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role not in ('manager', 'superadmin') or session.get('view_as_admin'):
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator that requires the user to be logged in AND have the 'admin' role."""
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role not in ('admin', 'superadmin'):
            abort(403)
        return f(*args, **kwargs)
    return decorated_function
