import os
import uuid
import csv
from flask import render_template, request, flash, redirect, url_for, current_app
from flask_login import current_user, login_required
from werkzeug.security import generate_password_hash
from app.blueprints.catalog import catalog_bp
from app.models import User, Building, Product, CsvUpload, OrderItem, InventoryMovement
from app.extensions import db
from app.utils.decorators import superadmin_required, admin_required, management_required


# ─────────────────────────────────────────────────────────────────────────────
# Assign Building to Admin
# ─────────────────────────────────────────────────────────────────────────────
@catalog_bp.route('/assign_building', methods=['GET', 'POST'])
@management_required
def assign_building():
    if request.method == 'POST':
        admin_id = request.form.get('admin_id')
        building_ids = request.form.getlist('building_ids')

        if admin_id and building_ids:
            admin = User.query.get(admin_id)
            if admin:
                assigned_names = []
                for b_id in building_ids:
                    if b_id and b_id != 'none':
                        building = Building.query.get(b_id)
                        if building:
                            building.admin_id = admin.id
                            assigned_names.append(building.name)
                db.session.commit()
                if assigned_names:
                    names_str = ", ".join(assigned_names)
                    flash(f'Edificios asignados a {admin.username} correctamente: {names_str}.', 'success')
                else:
                    flash('No se especificaron edificios válidos.', 'error')
            else:
                flash('Administrador no encontrado.', 'error')
        else:
            flash('Selecciona tanto al administrador como al menos un edificio.', 'error')
        return redirect(url_for('catalog.assign_building'))

    admins = User.query.filter_by(role='admin').all()
    buildings = Building.query.all()
    return render_template('catalog/assign_building.html', admins=admins, buildings=buildings)


# ─────────────────────────────────────────────────────────────────────────────
# Create New Building
# ─────────────────────────────────────────────────────────────────────────────
@catalog_bp.route('/buildings/new', methods=['GET', 'POST'])
@management_required
def create_building():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        address = request.form.get('address', '').strip()
        departments_count = request.form.get('departments_count', type=int, default=0)
        admin_id = request.form.get('admin_id') or None

        imagen_frontis = None
        if 'imagen_frontis' in request.files:
            file = request.files['imagen_frontis']
            if file.filename:
                ext = os.path.splitext(file.filename)[1]
                filename = f"{uuid.uuid4().hex}{ext}"
                upload_path = os.path.join(current_app.root_path, 'static', 'uploads')
                os.makedirs(upload_path, exist_ok=True)
                file.save(os.path.join(upload_path, filename))
                imagen_frontis = filename

        if not name:
            flash('El nombre del edificio es obligatorio.', 'error')
            return redirect(url_for('catalog.create_building'))

        existing = Building.query.filter_by(name=name).first()
        if existing:
            flash(f'Ya existe un edificio con el nombre "{name}".', 'error')
            return redirect(url_for('catalog.create_building'))

        building = Building(name=name, address=address, departments_count=departments_count, admin_id=int(admin_id) if admin_id else None, imagen_frontis=imagen_frontis)
        db.session.add(building)
        db.session.commit()
        flash(f'Edificio "{name}" creado correctamente.', 'success')
        return redirect(url_for('catalog.list_buildings'))

    admins = User.query.filter_by(role='admin').all()
    return render_template('catalog/create_building.html', admins=admins)


# ─────────────────────────────────────────────────────────────────────────────
# List Buildings
# ─────────────────────────────────────────────────────────────────────────────
@catalog_bp.route('/buildings', methods=['GET'])
@management_required
def list_buildings():
    buildings = Building.query.all()
    return render_template('catalog/list_buildings_admin.html', buildings=buildings)


# ─────────────────────────────────────────────────────────────────────────────
# Edit Building
# ─────────────────────────────────────────────────────────────────────────────
@catalog_bp.route('/buildings/<int:building_id>/edit', methods=['GET', 'POST'])
@management_required
def edit_building(building_id):
    building = Building.query.get_or_404(building_id)
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        address = request.form.get('address', '').strip()
        departments_count = request.form.get('departments_count', type=int, default=0)
        admin_id = request.form.get('admin_id')

        if not name:
            flash('El nombre del edificio es obligatorio.', 'error')
            return redirect(url_for('catalog.edit_building', building_id=building.id))

        existing = Building.query.filter(Building.name == name, Building.id != building.id).first()
        if existing:
            flash(f'Ya existe un edificio con el nombre "{name}".', 'error')
            return redirect(url_for('catalog.edit_building', building_id=building.id))

        if 'imagen_frontis' in request.files:
            file = request.files['imagen_frontis']
            if file.filename:
                ext = os.path.splitext(file.filename)[1]
                filename = f"{uuid.uuid4().hex}{ext}"
                upload_path = os.path.join(current_app.root_path, 'static', 'uploads')
                os.makedirs(upload_path, exist_ok=True)
                file.save(os.path.join(upload_path, filename))
                building.imagen_frontis = filename

        building.name = name
        building.address = address
        building.departments_count = departments_count
        building.admin_id = int(admin_id) if admin_id and admin_id != 'none' else None

        db.session.commit()
        flash(f'Edificio "{name}" actualizado correctamente.', 'success')
        return redirect(url_for('catalog.list_buildings'))

    admins = User.query.filter_by(role='admin').all()
    return render_template('catalog/edit_building.html', building=building, admins=admins)


# ─────────────────────────────────────────────────────────────────────────────
# Delete Building
# ─────────────────────────────────────────────────────────────────────────────
@catalog_bp.route('/buildings/<int:building_id>/delete', methods=['POST'])
@management_required
def delete_building(building_id):
    building = Building.query.get_or_404(building_id)
    
    # Check if building has orders (basic protection)
    if building.orders:
        flash('No se puede eliminar este edificio porque tiene pedidos asociados.', 'error')
        return redirect(url_for('catalog.list_buildings'))

    db.session.delete(building)
    db.session.commit()
    flash(f'Edificio "{building.name}" eliminado correctamente.', 'success')
    return redirect(url_for('catalog.list_buildings'))

# ─────────────────────────────────────────────────────────────────────────────
# Create New Admin User
# ─────────────────────────────────────────────────────────────────────────────
@catalog_bp.route('/admins/new', methods=['GET', 'POST'])
@management_required
def create_admin():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        confirm  = request.form.get('confirm_password', '').strip()
        role = request.form.get('role', 'admin')

        if not username or not password:
            flash('Usuario y contraseña son obligatorios.', 'error')
            return redirect(url_for('catalog.create_admin'))

        if role not in ['admin', 'manager']:
            flash('El rol seleccionado no es válido.', 'error')
            return redirect(url_for('catalog.create_admin'))

        if role == 'manager' and current_user.role != 'superadmin':
            flash('Solo un Superadmin puede asignar el rol de Manager.', 'error')
            return redirect(url_for('catalog.create_admin'))

        if password != confirm:
            flash('Las contraseñas no coinciden.', 'error')
            return redirect(url_for('catalog.create_admin'))

        if len(password) < 6:
            flash('La contraseña debe tener al menos 6 caracteres.', 'error')
            return redirect(url_for('catalog.create_admin'))

        existing = User.query.filter_by(username=username).first()
        if existing:
            flash(f'Ya existe un usuario con el nombre "{username}".', 'error')
            return redirect(url_for('catalog.create_admin'))

        new_user = User(username=username, name=name, role=role)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash(f'Administrador "{username}" creado correctamente.', 'success')
        return redirect(url_for('catalog.list_admins'))

    return render_template('catalog/create_admin.html')


# ─────────────────────────────────────────────────────────────────────────────
# List Admins
# ─────────────────────────────────────────────────────────────────────────────
@catalog_bp.route('/admins', methods=['GET'])
@management_required
def list_admins():
    admins = User.query.filter(User.role.in_(['admin', 'manager'])).all()
    # Find active building for each admin if any
    admin_buildings = {}
    for admin in admins:
        admin_buildings[admin.id] = [b.name for b in admin.assigned_buildings]
    return render_template('catalog/list_admins.html', admins=admins, admin_buildings=admin_buildings)


# ─────────────────────────────────────────────────────────────────────────────
# Edit Admin
# ─────────────────────────────────────────────────────────────────────────────
@catalog_bp.route('/admins/<int:admin_id>/edit', methods=['GET', 'POST'])
@management_required
def edit_admin(admin_id):
    admin = User.query.get_or_404(admin_id)
    if admin.role == 'superadmin':
        flash('No puedes editar cuentas de Superadmin.', 'error')
        return redirect(url_for('catalog.list_admins'))

    if admin.role == 'manager' and current_user.role != 'superadmin' and current_user.id != admin.id:
        flash('Solo un Superadmin puede editar a otros Managers.', 'error')
        return redirect(url_for('catalog.list_admins'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        role = request.form.get('role')
        building_ids = request.form.getlist('building_ids')

        if not name or not username:
            flash('Nombre y usuario son obligatorios.', 'error')
            return redirect(url_for('catalog.edit_admin', admin_id=admin.id))

        existing = User.query.filter(User.username == username, User.id != admin.id).first()
        if existing:
            flash(f'Ya existe un usuario con el nombre "{username}".', 'error')
            return redirect(url_for('catalog.edit_admin', admin_id=admin.id))

        admin.name = name
        admin.username = username
        
        if role in ['admin', 'manager']:
            if role == 'manager' and current_user.role != 'superadmin':
                flash('Solo un Superadmin puede asignar el rol de Manager.', 'error')
                return redirect(url_for('catalog.edit_admin', admin_id=admin.id))
            admin.role = role

        if password:
            if len(password) < 6:
                flash('La nueva contraseña debe tener al menos 6 caracteres.', 'error')
            else:
                admin.set_password(password)

        # Clear existing assignments explicitly
        for b in admin.assigned_buildings:
            b.admin_id = None
        
        # Apply new ones from the checkboxes
        for b_id in building_ids:
            if b_id and b_id != 'none':
                bldg = Building.query.get(b_id)
                if bldg:
                    bldg.admin_id = admin.id

        db.session.commit()
        flash(f'Administrador "{name}" actualizado correctamente.', 'success')
        return redirect(url_for('catalog.list_admins'))

    buildings = Building.query.all()
    # Get current building if assigned
    current_building = admin.assigned_buildings[0] if admin.assigned_buildings else None
    return render_template('catalog/edit_admin.html', admin=admin, buildings=buildings, current_building=current_building)


# ─────────────────────────────────────────────────────────────────────────────
# Delete Admin
# ─────────────────────────────────────────────────────────────────────────────
@catalog_bp.route('/admins/<int:admin_id>/delete', methods=['POST'])
@management_required
def delete_admin(admin_id):
    admin = User.query.get_or_404(admin_id)
    if admin.role == 'superadmin':
        flash('No se puede eliminar a un Superadmin.', 'error')
        return redirect(url_for('catalog.list_admins'))

    # Detach buildings
    for b in admin.assigned_buildings:
        b.admin_id = None

    db.session.delete(admin)
    db.session.commit()
    flash(f'Administrador {admin.username} eliminado correctamente.', 'success')
    return redirect(url_for('catalog.list_admins'))

# ─────────────────────────────────────────────────────────────────────────────
# CSV Upload for Product Catalog
# ─────────────────────────────────────────────────────────────────────────────
@catalog_bp.route('/upload', methods=['GET', 'POST'])
@management_required
def upload_csv():
    """Upload a CSV file to create or update products in the master catalog."""
    if request.method == 'POST':
        if 'csv_file' not in request.files:
            flash('No se seleccionó ningún archivo.', 'error')
            return redirect(url_for('catalog.upload_csv'))

        file = request.files['csv_file']
        if file.filename == '':
            flash('No se seleccionó ningún archivo.', 'error')
            return redirect(url_for('catalog.upload_csv'))

        if not file.filename.lower().endswith('.csv'):
            flash('El archivo debe ser un CSV (.csv).', 'error')
            return redirect(url_for('catalog.upload_csv'))

        try:
            file_bytes = file.stream.read()
            try:
                decoded_text = file_bytes.decode('utf-8-sig')
            except UnicodeDecodeError:
                decoded_text = file_bytes.decode('cp1252', errors='replace')
            
            stream = io.StringIO(decoded_text)
            
            # Detectar si es coma o punto y coma
            sample = stream.read(1024)
            stream.seek(0)
            dialect = csv.Sniffer().sniff(sample, delimiters=',;')
            
            reader = csv.DictReader(stream, dialect=dialect)
            created_count = 0
            updated_count = 0
            error_rows = []
            
            # Create the upload record
            import datetime
            new_upload = CsvUpload(filename=file.filename)
            db.session.add(new_upload)
            db.session.flush()

            for row_num, row in enumerate(reader, start=2):
                try:
                    sku        = row.get('sku', '').strip()
                    nombre     = row.get('nombre', '').strip()
                    unidad     = row.get('unidad_medida', '').strip()
                    precio_str = row.get('precio', '0').strip()
                    descripcion = row.get('descripcion', '').strip()
                    categoria  = row.get('categoria', 'General').strip()
                    imagen_url = row.get('imagen_url', '').strip()
                    stock_str  = row.get('stock_actual', '0').strip()

                    if not nombre:
                        error_rows.append(f"Fila {row_num}: nombre vacío")
                        continue

                    precio = float(precio_str) if precio_str else 0.0
                    stock  = int(stock_str) if stock_str else 0

                    product = None
                    if sku:
                        product = Product.query.filter_by(sku=sku).first()
                    if not product:
                        product = Product.query.filter_by(name=nombre).first()

                    if product:
                        if sku:
                            product.sku = sku
                        product.name   = nombre
                        if unidad:
                            product.unit = unidad
                        product.precio = precio
                        if descripcion:
                            product.description = descripcion
                        if categoria:
                            product.categoria = categoria
                        if imagen_url:
                            product.imagen_url = imagen_url
                        if stock > 0:
                            product.stock_actual = stock
                        updated_count += 1
                    else:
                        new_product = Product(
                            sku=sku if sku else None,
                            name=nombre,
                            unit=unidad if unidad else 'Unidad',
                            categoria=categoria if categoria else 'General',
                            precio=precio,
                            description=descripcion if descripcion else None,
                            imagen_url=imagen_url if imagen_url else '/static/img/default-product.png',
                            stock_actual=stock,
                            source_csv_id=new_upload.id
                        )
                        db.session.add(new_product)
                        created_count += 1
                except Exception as e:
                    error_rows.append(f"Fila {row_num}: {str(e)}")
                    continue
                    
            new_upload.products_created = created_count
            new_upload.products_updated = updated_count
            db.session.commit()
            parts = []
            if created_count:
                parts.append(f'{created_count} producto(s) creado(s)')
            if updated_count:
                parts.append(f'{updated_count} producto(s) actualizado(s)')
            if parts:
                flash(f'CSV procesado: {", ".join(parts)}.', 'success')
            else:
                flash('No se procesaron productos del CSV.', 'info')
            if error_rows:
                flash(f'Errores: {"; ".join(error_rows[:5])}', 'error')

        except Exception as e:
            db.session.rollback()
            flash(f'Error al procesar el CSV: {str(e)}', 'error')

        return redirect(url_for('catalog.upload_csv'))

    products = Product.query.filter_by(is_active=True).order_by(Product.name).all()
    uploads = CsvUpload.query.order_by(CsvUpload.uploaded_at.desc()).all()
    return render_template('catalog/upload_csv.html', products=products, uploads=uploads)

@catalog_bp.route('/upload/<int:upload_id>/delete', methods=['POST'])
@management_required
def delete_csv_upload(upload_id):
    upload = CsvUpload.query.get_or_404(upload_id)
    products = Product.query.filter_by(source_csv_id=upload.id).all()
    deleted_count = 0
    soft_deleted_count = 0

    for p in products:
        has_orders = OrderItem.query.filter_by(product_id=p.id).first() is not None
        has_movements = InventoryMovement.query.filter_by(product_id=p.id).first() is not None

        if has_orders or has_movements:
            p.is_active = False
            soft_deleted_count += 1
        else:
            db.session.delete(p)
            deleted_count += 1

    db.session.delete(upload)
    db.session.commit()
    flash(f'Lote eliminado. {deleted_count} borrados definitivos, {soft_deleted_count} ocultados por seguridad.', 'success')
    return redirect(url_for('catalog.upload_csv'))

# ─────────────────────────────────────────────────────────────────────────────
# Local Warehouse (Products CRUD)
# ─────────────────────────────────────────────────────────────────────────────
@catalog_bp.route('/warehouse', methods=['GET'])
@management_required
def warehouse():
    products = Product.query.order_by(Product.name).all()
    return render_template('catalog/warehouse.html', products=products)

@catalog_bp.route('/warehouse/product/new', methods=['GET', 'POST'])
@management_required
def create_product():
    if request.method == 'POST':
        sku = request.form.get('sku', '').strip()
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        unit = request.form.get('unit', '').strip()
        precio = request.form.get('precio', type=float, default=0.0)
        stock = request.form.get('stock_actual', type=int, default=0)
        
        imagen_url = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                ext = os.path.splitext(file.filename)[1]
                filename = f"prod_{uuid.uuid4().hex}{ext}"
                upload_path = os.path.join(current_app.root_path, 'static', 'uploads')
                os.makedirs(upload_path, exist_ok=True)
                file.save(os.path.join(upload_path, filename))
                imagen_url = f'/static/uploads/{filename}'
        
        if not name:
            flash('El nombre del producto es obligatorio.', 'error')
            return redirect(url_for('catalog.create_product'))
            
        product = Product(sku=sku if sku else None, name=name, description=description, unit=unit, precio=precio, stock_actual=stock)
        if imagen_url:
            product.imagen_url = imagen_url
            
        db.session.add(product)
        db.session.commit()
        flash(f'Producto "{name}" creado correctamente.', 'success')
        return redirect(url_for('catalog.warehouse'))
        
    return render_template('catalog/create_product.html')

@catalog_bp.route('/warehouse/product/<int:product_id>/edit', methods=['GET', 'POST'])
@management_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    if request.method == 'POST':
        product.sku = request.form.get('sku', '').strip() or None
        product.name = request.form.get('name', '').strip()
        product.description = request.form.get('description', '').strip()
        product.unit = request.form.get('unit', '').strip()
        product.precio = request.form.get('precio', type=float, default=0.0)
        product.stock_actual = request.form.get('stock_actual', type=int, default=0)
        
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                ext = os.path.splitext(file.filename)[1]
                filename = f"prod_{uuid.uuid4().hex}{ext}"
                upload_path = os.path.join(current_app.root_path, 'static', 'uploads')
                os.makedirs(upload_path, exist_ok=True)
                file.save(os.path.join(upload_path, filename))
                product.imagen_url = f'/static/uploads/{filename}'
        
        db.session.commit()
        flash(f'Producto "{product.name}" actualizado correctamente.', 'success')
        return redirect(url_for('catalog.warehouse'))
        
    return render_template('catalog/edit_product.html', product=product)

@catalog_bp.route('/warehouse/product/<int:product_id>/toggle', methods=['POST'])
@management_required
def toggle_product(product_id):
    product = Product.query.get_or_404(product_id)
    product.is_active = not product.is_active
    db.session.commit()
    status = 'activado' if product.is_active else 'desactivado'
    flash(f'Producto "{product.name}" {status} correctamente.', 'success')
    return redirect(url_for('catalog.warehouse'))
