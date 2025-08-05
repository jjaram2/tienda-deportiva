from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app import db
# from app.models.products import Product  # Asume que tienes un modelo Product

bp = Blueprint('store', __name__)

@bp.route('/home')
def home():
    from flask_login import current_user
    if hasattr(current_user, 'is_authenticated') and current_user.is_authenticated:
        # Redirige a la vista del rol correspondiente
        if current_user.role == 'admin':
            return redirect(url_for('admin.admin_dashboard'))
        elif current_user.role == 'vendedor':
            return redirect(url_for('auth.dashboard'))
        elif current_user.role == 'proveedor':
            return redirect(url_for('auth.dashboard'))
        else:
            return redirect(url_for('auth.dashboard'))
    productos = []  # Simulación
    return render_template('home.html', productos=productos)

@bp.route('/categorias')
def categorias():
    categorias = [
        {'nombre': 'Deportes de Raqueta', 'url': '/categoria/raqueta'},
        {'nombre': 'Camping', 'url': '/categoria/camping'},
        {'nombre': 'Sportswear', 'url': '/categoria/sportswear'},
        {'nombre': 'Accesorios', 'url': '/categoria/accesorios'}
    ]
    return render_template('categorias.html', categorias=categorias)

@bp.route('/categoria/<nombre>')
def categoria(nombre):
    # productos = Product.query.filter_by(categoria=nombre).all()
    productos = []  # Simulación
    return render_template('categorias.html', productos=productos, categoria=nombre)

@bp.route('/producto/<int:id>')
def producto(id):
    # producto = Product.query.get_or_404(id)
    producto = {'id': id, 'nombre': 'Producto demo', 'descripcion': 'Descripción', 'precio': 100, 'imagen_url': '#'}
    return render_template('producto.html', producto=producto)

@bp.route('/carrito')
def carrito():
    carrito = session.get('carrito', [])
    total = sum(item['precio'] * item['cantidad'] for item in carrito) if carrito else 0
    return render_template('carrito.html', carrito=carrito, total=total)

@bp.route('/carrito/agregar/<int:id>', methods=['POST'])
def agregar_carrito(id):
    # producto = Product.query.get_or_404(id)
    producto = {'id': id, 'nombre': 'Producto demo', 'precio': 100}
    cantidad = int(request.form.get('cantidad', 1))
    item = {'id': id, 'nombre': producto['nombre'], 'precio': producto['precio'], 'cantidad': cantidad}
    carrito = session.get('carrito', [])
    carrito.append(item)
    session['carrito'] = carrito
    flash('Producto agregado al carrito', 'success')
    return redirect(url_for('store.carrito'))

@bp.route('/carrito/eliminar/<int:id>')
def eliminar_carrito(id):
    carrito = session.get('carrito', [])
    carrito = [item for item in carrito if item['id'] != id]
    session['carrito'] = carrito
    flash('Producto eliminado del carrito', 'info')
    return redirect(url_for('store.carrito'))
