from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models.users import Users

bp = Blueprint('auth', __name__)

@bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nameUser = request.form['nameUser']
        passwordUser = request.form['passwordUser']
        
        user = Users.query.filter_by(nameUser=nameUser).first()
        if user:
            from werkzeug.security import check_password_hash
            if check_password_hash(user.passwordUser, passwordUser):
                login_user(user)
                flash("Login successful!", "success")
                return redirect(url_for('auth.dashboard'))
        flash('Invalid credentials. Please try again.', 'danger')
    
    if current_user.is_authenticated:
        # Redirige a la vista del rol correspondiente
        if current_user.role == 'admin':
            return redirect(url_for('admin.admin_dashboard'))
        elif current_user.role == 'vendedor':
            return redirect(url_for('auth.dashboard'))  # asume que dashboard redirige a vendedor_dashboard
        elif current_user.role == 'proveedor':
            return redirect(url_for('auth.dashboard'))  # asume que dashboard redirige a proveedor_dashboard
        else:
            return redirect(url_for('auth.dashboard'))
    return render_template("login.html")

@bp.route('/dashboard')
@login_required
def dashboard():    
    if current_user.role == 'admin':
        return render_template('admin_dashboard.html')
    elif current_user.role == 'vendedor':
        return render_template('vendedor_dashboard.html')
    elif current_user.role == 'proveedor':
        return render_template('proveedor_dashboard.html')
    else:
        return render_template('user_dashboard.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
