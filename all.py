# factory_app/__init__.py(Factory Application Pattern)
# factory_app__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config import Config

db = SQLAlchemy()
limiter = Limiter(key_func=get_remote_address)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    limiter.init_app(app)

    with app.app_context():
        from.employee import employee_bp
        from.product import product_bp
        from.order import order_bp
        from.customer import customer_bp
        from.production import production_bp

        # Register Blueprints
        app.register_blueprint(employee_bp)
        app.register_blueprint(product_bp)
        app.register_blueprint(order_bp)
        app.register_blueprint(customer_bp)
        app.register_blueprint(production_bp)

        db.create_all() # Create database tables for our data models

    return app

# factory_app/models.py (SQLAlchemy Models)
# factory_app/models.py
from flask_sqlalchemy import AQLAlchemy

db = SQLAlchemy()
class Employee(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)

class product(db.Model):
    __tablename__ ='products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

class order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.foreignKey('customer.id'), nullable=False)
    product_id = db.Column(db.Integer, db.foreignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)

class Customer(db.Model):
    __tablename__ = 'customer'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)

class Production(db.Model):
    __tablename__ = 'production'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.foreignKey('product.id'), nullable=False)
    quantity_produced = db.Column(db.Integer, nullable=False)
    data_produced = db.Column(db.Date, nullable=False)

# factory_app/config.py(Configuration Setting)
class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///factory.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RATELIMIT_HEADERS_ENABLED = True
    DEFAULT_RATE_LIMIT = "100/hour"

# factory_app/employee.py(Employee Blueprint)
from flask import Blueprint, jsonify, request
from.models import db, Employee

employee_bp = Blueprint('employee', __name__, url_prefix='/employees')

@employee_bp.route('/', methods=['POST'])
def create_employee():
    data = request.get_json()
    employee = Employee(name=data['name'], position=data['position'])
    db.session.add(employee)
    db.session.commit()
    return jsonify({'id': employee.id, 'name': employee.name, 'position': employee.position}), 201

@employee_bp.route('/', methods=['GET'])
def get_all_employees():
    employees = Employee.query.all()
    return jsonify([{'id': emp.id, 'name': emp.name, 'position': emp.position} for emp in employees])


# factory_app/product.py(Product Blueprint)
from flask import Blueprint, jsonify, request
from .models import db, Product

product_bp = Blueprint('product', __name__, url_prefix='/products')

@product_bp.route('/', methods=['POST'])
def create_product():
    data = request.get_json()
    product = product(name=data['name'], price=data['price'])
    db.session.add(product)
    db.session.commit()
    return jsonify({'id': product.id, 'name': product.name, 'price': product.price}), 201

@product_bp.route('/', methods=['GET'])
def get_all_products():
    products = product.query.all()
    return jsonify([{'id': p.id, 'name': p.name, 'price': p.price} for p in products])

# factory_app/order.py (Order Blueprint)
from flask import Blueprint, jsonify, request
from .models import db, Order

order_bp = Blueprint('order', __name__, url_prefix='/orders')

@order_bp.route('/', methods=['POST'])
def create_order():
    data = request.get_json()
    order = Order(customer_id=data['customer_id'], product_id=data['product_id'], quantity=data['quantity'], total_price=data['total_price'])
    db.session.add(order)
    db.session.commit()
    return jsonify({'id': order.id, 'customer_id': order.customer_id, 'product_id': order.product_id, 'quantity': order.quantity, 'total_price': order.total_price}), 201

@order_bp.route('/', methods=['GET'])
def get_all_orders():
    orders = Order.query.all()
    return jsonify([{'id': o.id, 'customer_id': o.customer_id, 'product_id': o.product_id, 'quantity': o.quantity, 'total_price': o.total_price} for o in orders])


# factory_app/customer.py (Customer Blueprint)
# factory_app/customer.py
from flask import Blueprint, jsonify, request
from .models import db, Customer

customer_bp = Blueprint('customer', __name__, url_prefix='/customer')

@customer_bp.route('/', methods=['POST'])
def create_customer():
    data = request.get_json()
    customer = Customer(name=data['name'], email=data['email'], phone=data['phone'])
    db.session.add(customer)
    db.session.commit()
    return jsonify({'id': customer.id, 'name': customer.name, 'email': customer.email, 'phone': customer.phone}), 201

@customer_bp.route('/', methods=['GET'])
def get_all_customers():
    customers = Customer.query.all()
    return jsonify([{'id': c.id, 'name': c.name, 'email': c.email, 'phone': c.phone} for c in customers])

# factory_app/production.py (Production Blueprint)
# factory_app/production.py
from falsk import Blueprint, jsonify, request
from .models import db, Production

production_bp = Blueprint('production', __name__, url_prefix='/production')

@production_bp.route('/', methods=['POST'])
def create_production():
    data = request.get_json()
    production = Production(product_id=data['product_id'], quantity_produced=data['quantity_produced'], date_produced=data['date_produced'])
    db.session.add(production)
    db.session.commit()
    return jsonify({'id': production.id, 'product_id': production.product_id, 'quantity_produced': production.quantity_produced, 'date_produced': production.date_produced}), 201

@production_bp.route('/', methods=['GET'])
def get_all_production():
    productions = Production.query.all()
    return jsonify([{'id': p.id, 'product_id': p.product_id, 'quantity_produced': p.quantity_produced, 'date_produced': p.date_produced} for p in productions])

# app.py (Main Entry Point)
# app.py
from factory_app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)







