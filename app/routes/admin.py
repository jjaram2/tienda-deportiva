from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.models.users import Users
from app import db

bp = Blueprint('admin', __name__)

@bp.route('/admin')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        flash('Acceso denegado.', 'danger')
        return redirect(url_for('auth.dashboard'))
    users = Users.query.all()
    return render_template('admin_dashboard.html', users=users)

@bp.route('/admin/bloquear/<int:id>')
@login_required
def bloquear_usuario(id):
    if current_user.role != 'admin':
        flash('Acceso denegado.', 'danger')
        return redirect(url_for('auth.dashboard'))
    user = Users.query.get_or_404(id)
    user.role = 'bloqueado'
    db.session.commit()
    flash('Usuario bloqueado.', 'info')
    return redirect(url_for('admin.admin_dashboard'))

@bp.route('/admin/cambiar_rol/<int:id>', methods=['POST'])
@login_required
def cambiar_rol(id):
    if current_user.role != 'admin':
        flash('Acceso denegado.', 'danger')
        return redirect(url_for('auth.dashboard'))
    user = Users.query.get_or_404(id)
    nuevo_rol = request.form.get('nuevo_rol')
    if nuevo_rol in ['admin', 'vendedor', 'usuario', 'proveedor']:
        user.role = nuevo_rol
        db.session.commit()
        flash('Rol actualizado.', 'success')
    else:
        flash('Rol inválido.', 'danger')
    return redirect(url_for('admin.admin_dashboard'))

@bp.route('/admin/aceptar_pedido/<int:id>')
@login_required
def aceptar_pedido(id):
    if current_user.role != 'admin':
        flash('Acceso denegado.', 'danger')
        return redirect(url_for('auth.dashboard'))
    # Aquí iría la lógica para aceptar el pedido del proveedor
    flash('Pedido aceptado.', 'success')
    return redirect(url_for('admin.admin_dashboard'))
