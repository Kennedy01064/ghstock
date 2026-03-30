from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, Table, Date
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from backend.db.session import Base

# Association table between DispatchBatch and Order
dispatch_batch_orders = Table('dispatch_batch_orders', Base.metadata,
    Column('dispatch_batch_id', Integer, ForeignKey('dispatch_batch.id'), primary_key=True),
    Column('order_id', Integer, ForeignKey('order.id'), primary_key=True)
)

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(80), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=True)
    password_hash = Column(String(256), nullable=False)
    role = Column(String(20), nullable=False, default='admin')  # 'superadmin' OR 'admin'

    # Reverse relationship for assigned buildings
    assigned_buildings = relationship('Building', backref='admin', lazy=True)

    def __repr__(self):
        return f'<User {self.username} ({self.role})>'


class Building(Base):
    __tablename__ = "building"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), unique=True, nullable=False, index=True)
    address = Column(String(255))
    departments_count = Column(Integer, default=0)
    admin_id = Column(Integer, ForeignKey('user.id'), nullable=True)
    imagen_frontis = Column(String(255), nullable=True)

    # Relationship to orders
    orders = relationship('Order', backref='building', lazy=True)

    def __repr__(self):
        return f'<Building {self.name}>'


class CsvUpload(Base):
    __tablename__ = "csv_upload"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    uploaded_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    products_created = Column(Integer, default=0)
    products_updated = Column(Integer, default=0)

    # Relationship to products
    products = relationship('Product', backref='source_csv', lazy=True)


class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(50), unique=True, nullable=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    categoria = Column(String(100), nullable=True, default='General')
    description = Column(Text, nullable=True)
    unit = Column(String(20))  # e.g., 'liters', 'units', 'boxes'
    precio = Column(Float, nullable=True, default=0.0)
    imagen_url = Column(String(255), nullable=True, default='/static/img/default-product.png')
    stock_actual = Column(Integer, nullable=False, default=0)
    stock_minimo = Column(Integer, nullable=False, default=10)
    is_active = Column(Boolean, default=True)
    
    source_csv_id = Column(Integer, ForeignKey('csv_upload.id'), nullable=True)


class Order(Base):
    __tablename__ = "order"
    id = Column(Integer, primary_key=True, index=True)
    building_id = Column(Integer, ForeignKey('building.id'), nullable=False)
    created_by_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    status = Column(String(20), default='draft')  # 'draft', 'submitted', 'processing', 'dispatched'

    # Relationships
    items = relationship('OrderItem', backref='order', lazy=True, cascade="all, delete-orphan")
    created_by = relationship('User', foreign_keys=[created_by_id])


class OrderItem(Base):
    __tablename__ = "order_item"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('order.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)

    nombre_producto_snapshot = Column(String(100), nullable=True)
    precio_unitario = Column(Float, nullable=True, default=0.0)

    # Relationship to product
    product = relationship('Product')


class DispatchBatch(Base):
    __tablename__ = "dispatch_batch"
    id = Column(Integer, primary_key=True, index=True)
    created_by_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    status = Column(String(20), default='pending')  # 'pending', 'dispatched'

    # Relationships
    orders = relationship('Order', secondary=dispatch_batch_orders, lazy='subquery',
        backref='batches')
    items = relationship('DispatchBatchItem', backref='batch', lazy=True, cascade="all, delete-orphan")
    created_by = relationship('User', foreign_keys=[created_by_id])


class DispatchBatchItem(Base):
    __tablename__ = "dispatch_batch_item"
    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(Integer, ForeignKey('dispatch_batch.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    total_quantity = Column(Integer, nullable=False)

    # Relationship to product
    product = relationship('Product')


class InventoryMovement(Base):
    __tablename__ = "inventory_movement"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    quantity = Column(Integer, nullable=False)  # Can be positive or negative
    movement_type = Column(String(20), nullable=False)  # 'in', 'out'
    reference_id = Column(Integer, nullable=True)  # e.g., batch_id
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    created_by_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    # Relationships
    product = relationship('Product')
    created_by = relationship('User', foreign_keys=[created_by_id])


class BuildingInventory(Base):
    __tablename__ = "building_inventory"
    id = Column(Integer, primary_key=True, index=True)
    building_id = Column(Integer, ForeignKey('building.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    quantity = Column(Integer, nullable=False, default=0)
    last_updated = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    building = relationship('Building', backref='inventory_items')
    product = relationship('Product')


class ConsumptionLog(Base):
    __tablename__ = "consumption_log"
    id = Column(Integer, primary_key=True, index=True)
    building_id = Column(Integer, ForeignKey('building.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    reported_by_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    quantity_consumed = Column(Integer, nullable=False)
    reported_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    building = relationship('Building')
    product = relationship('Product')
    reported_by = relationship('User', foreign_keys=[reported_by_id])


class Purchase(Base):
    __tablename__ = "purchase"
    id = Column(Integer, primary_key=True, index=True)
    supplier = Column(String(150), nullable=True)
    invoice_number = Column(String(50), nullable=True)
    purchase_date = Column(Date, nullable=False)
    total_amount = Column(Float, nullable=True, default=0.0)
    notes = Column(Text, nullable=True)
    created_by_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    items = relationship('PurchaseItem', backref='purchase', lazy=True, cascade="all, delete-orphan")
    created_by = relationship('User', foreign_keys=[created_by_id])


class PurchaseItem(Base):
    __tablename__ = "purchase_item"
    id = Column(Integer, primary_key=True, index=True)
    purchase_id = Column(Integer, ForeignKey('purchase.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=True, default=0.0)

    product = relationship('Product')
