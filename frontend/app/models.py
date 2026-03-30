from app.extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone

# Association table between DispatchBatch and Order
dispatch_batch_orders = db.Table('dispatch_batch_orders',
    db.Column('dispatch_batch_id', db.Integer, db.ForeignKey('dispatch_batch.id'), primary_key=True),
    db.Column('order_id', db.Integer, db.ForeignKey('order.id'), primary_key=True)
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=True)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='admin')  # 'superadmin' OR 'admin'

    # Reverse relationship for assigned buildings
    assigned_buildings = db.relationship('Building', backref='admin', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username} ({self.role})>'


class Building(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    address = db.Column(db.String(255))
    departments_count = db.Column(db.Integer, default=0)
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    imagen_frontis = db.Column(db.String(255), nullable=True)

    # Relationship to orders
    orders = db.relationship('Order', backref='building', lazy=True)

    def __repr__(self):
        return f'<Building {self.name}>'


class CsvUpload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    products_created = db.Column(db.Integer, default=0)
    products_updated = db.Column(db.Integer, default=0)

    # Relationship to products
    products = db.relationship('Product', backref='source_csv', lazy=True)

    def __repr__(self):
        return f'<CsvUpload {self.filename}>'


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(50), unique=True, nullable=True)
    name = db.Column(db.String(100), nullable=False)
    categoria = db.Column(db.String(100), nullable=True, default='General')
    description = db.Column(db.Text, nullable=True)
    unit = db.Column(db.String(20))  # e.g., 'liters', 'units', 'boxes'
    precio = db.Column(db.Float, nullable=True, default=0.0)
    imagen_url = db.Column(db.String(255), nullable=True, default='/static/img/default-product.png')
    stock_actual = db.Column(db.Integer, nullable=False, default=0)
    stock_minimo = db.Column(db.Integer, nullable=False, default=10)
    is_active = db.Column(db.Boolean, default=True)
    
    source_csv_id = db.Column(db.Integer, db.ForeignKey('csv_upload.id'), nullable=True)

    def __repr__(self):
        return f'<Product {self.name}>'


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    building_id = db.Column(db.Integer, db.ForeignKey('building.id'), nullable=False)
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    status = db.Column(db.String(20), default='draft')  # 'draft', 'submitted', 'processing', 'dispatched'

    # Relationships
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade="all, delete-orphan")
    created_by = db.relationship('User', foreign_keys=[created_by_id])

    def __repr__(self):
        return f'<Order {self.id} - {self.status}>'


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)

    # ── Security: Historical snapshot fields ──────────────────────────────────
    # These are written ONCE at item-creation time and NEVER updated again.
    # They preserve the exact product name and price at the moment of the order,
    # regardless of future catalog changes.
    nombre_producto_snapshot = db.Column(db.String(100), nullable=True)
    precio_unitario = db.Column(db.Float, nullable=True, default=0.0)
    # ─────────────────────────────────────────────────────────────────────────

    # Relationship to product (still useful for the catalog view / stock reads)
    product = db.relationship('Product')

    @property
    def display_name(self):
        """Return the snapshotted name if available, fall back to live product name."""
        return self.nombre_producto_snapshot or (self.product.name if self.product else 'Producto eliminado')

    @property
    def display_price(self):
        """Return the snapshotted unit price if available, fall back to live product price."""
        if self.precio_unitario is not None:
            return self.precio_unitario
        return self.product.precio if self.product else 0.0

    def __repr__(self):
        return f'<OrderItem {self.display_name} x{self.quantity}>'


class DispatchBatch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    status = db.Column(db.String(20), default='pending')  # 'pending', 'dispatched'

    # Relationships
    orders = db.relationship('Order', secondary=dispatch_batch_orders, lazy='subquery',
        backref=db.backref('batches', lazy=True))
    items = db.relationship('DispatchBatchItem', backref='batch', lazy=True, cascade="all, delete-orphan")
    created_by = db.relationship('User', foreign_keys=[created_by_id])


class DispatchBatchItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    batch_id = db.Column(db.Integer, db.ForeignKey('dispatch_batch.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    total_quantity = db.Column(db.Integer, nullable=False)

    # Relationship to product
    product = db.relationship('Product')


class InventoryMovement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)  # Can be positive or negative
    movement_type = db.Column(db.String(20), nullable=False)  # 'in', 'out'
    reference_id = db.Column(db.Integer, nullable=True)  # e.g., batch_id
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Relationships
    product = db.relationship('Product')
    created_by = db.relationship('User', foreign_keys=[created_by_id])

    def __repr__(self):
        return f'<InventoryMovement {self.movement_type} {self.quantity} of Product {self.product_id}>'

class BuildingInventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    building_id = db.Column(db.Integer, db.ForeignKey('building.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    last_updated = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    building = db.relationship('Building', backref=db.backref('inventory', lazy=True, cascade="all, delete-orphan"))
    product = db.relationship('Product')

    def __repr__(self):
        return f'<BuildingInventory Building {self.building_id} Product {self.product_id} Qt {self.quantity}>'


class ConsumptionLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    building_id = db.Column(db.Integer, db.ForeignKey('building.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    reported_by_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quantity_consumed = db.Column(db.Integer, nullable=False)
    reported_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    building = db.relationship('Building')
    product = db.relationship('Product')
    reported_by = db.relationship('User', foreign_keys=[reported_by_id])

    def __repr__(self):
        return f'<ConsumptionLog Building {self.building_id} Product {self.product_id} Consumed {self.quantity_consumed}>'


class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    supplier = db.Column(db.String(150), nullable=True)
    invoice_number = db.Column(db.String(50), nullable=True)
    purchase_date = db.Column(db.Date, nullable=False)
    total_amount = db.Column(db.Float, nullable=True, default=0.0)
    notes = db.Column(db.Text, nullable=True)
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    items = db.relationship('PurchaseItem', backref='purchase', lazy=True, cascade="all, delete-orphan")
    created_by = db.relationship('User', foreign_keys=[created_by_id])

    def __repr__(self):
        return f'<Purchase {self.id} - {self.supplier}>'


class PurchaseItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    purchase_id = db.Column(db.Integer, db.ForeignKey('purchase.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Float, nullable=True, default=0.0)

    product = db.relationship('Product')

    @property
    def total_price(self):
        return self.quantity * (self.unit_price or 0.0)

    def __repr__(self):
        return f'<PurchaseItem {self.product.name} x{self.quantity}>'
