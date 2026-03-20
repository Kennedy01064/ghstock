from flask import render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
from app.blueprints.auth import auth_bp
from app.models import User


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Show login form and handle authentication."""
    # If user is already authenticated, redirect to dashboard
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        remember = request.form.get('remember') == 'on'

        if not username or not password:
            flash('Por favor ingresa tu usuario y contraseña.', 'error')
            return render_template('auth/login.html')

        user = User.query.filter_by(username=username).first()

        if user is None or not user.check_password(password):
            flash('Usuario o contraseña incorrectos. Inténtalo de nuevo.', 'error')
            return render_template('auth/login.html')

        # Successful authentication
        login_user(user, remember=remember)

        # Redirect to the page the user originally tried to access
        next_page = request.args.get('next')
        if next_page:
            return redirect(next_page)
        return redirect(url_for('dashboard.index'))

    return render_template('auth/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    """Log the current user out."""
    logout_user()
    flash('Has cerrado sesión correctamente.', 'success')
    return redirect(url_for('auth.login'))


@auth_bp.route('/toggle_role')
@login_required
def toggle_role():
    """Toggle superadmin to view the application as a regular admin."""
    if current_user.role == 'superadmin':
        if session.get('view_as_admin'):
            session.pop('view_as_admin', None)
            flash('Has regresado a la vista completa de Superadmin.', 'info')
        else:
            session['view_as_admin'] = True
            flash('Modo prueba activado. Estás viendo la plataforma como Administrador de Edificio.', 'info')
    return redirect(url_for('dashboard.index'))
