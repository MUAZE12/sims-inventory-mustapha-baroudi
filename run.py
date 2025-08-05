#!/usr/bin/env python3
"""
Smart Inventory Management System (SIMS)
Main application entry point
"""

import os
import click
from flask.cli import with_appcontext
from app import create_app, db
from app.models import Product, Category, Supplier, InventoryTransaction, Sale, SaleItem

# Create Flask application
app = create_app(os.getenv('FLASK_CONFIG') or 'default')

@app.shell_context_processor
def make_shell_context():
    """Make database models available in Flask shell"""
    return {
        'db': db,
        'Product': Product,
        'Category': Category,
        'Supplier': Supplier,
        'InventoryTransaction': InventoryTransaction,
        'Sale': Sale,
        'SaleItem': SaleItem
    }

@click.command()
@with_appcontext
def init_db():
    """Initialize the database with tables and sample data"""
    click.echo('Creating database tables...')
    db.create_all()
    
    # Create sample categories
    if not Category.query.first():
        click.echo('Adding sample categories...')
        categories = [
            Category(name='Textiles', description='Fabric and textile products'),
            Category(name='Electronics', description='Electronic devices and components'),
            Category(name='Office Supplies', description='Office and stationery items'),
            Category(name='Tools', description='Hardware and tools'),
        ]
        for category in categories:
            db.session.add(category)
    
    # Create sample suppliers
    if not Supplier.query.first():
        click.echo('Adding sample suppliers...')
        suppliers = [
            Supplier(
                name='Textile Morocco Ltd',
                contact_person='Ahmed Benali',
                email='ahmed@textilemorocco.ma',
                phone='+212-5-22-123456',
                address='Casablanca, Morocco'
            ),
            Supplier(
                name='Atlas Electronics',
                contact_person='Fatima Zahra',
                email='fatima@atlaselectronics.ma',
                phone='+212-5-37-789012',
                address='Rabat, Morocco'
            ),
        ]
        for supplier in suppliers:
            db.session.add(supplier)
    
    # Create sample products
    if not Product.query.first():
        click.echo('Adding sample products...')
        db.session.commit()  # Commit categories and suppliers first
        
        textile_category = Category.query.filter_by(name='Textiles').first()
        electronics_category = Category.query.filter_by(name='Electronics').first()
        textile_supplier = Supplier.query.filter_by(name='Textile Morocco Ltd').first()
        electronics_supplier = Supplier.query.filter_by(name='Atlas Electronics').first()
        
        products = [
            Product(
                name='Cotton Fabric - Blue',
                description='High-quality cotton fabric in blue color',
                sku='CTN-BLU-001',
                category_id=textile_category.id,
                supplier_id=textile_supplier.id,
                unit_price=25.50,
                cost_price=18.00,
                current_stock=150,
                reorder_level=30,
                safety_stock=10,
                unit_of_measure='meters'
            ),
            Product(
                name='LED Light Bulb 10W',
                description='Energy-efficient LED bulb, 10 watts',
                sku='LED-10W-001',
                category_id=electronics_category.id,
                supplier_id=electronics_supplier.id,
                unit_price=45.00,
                cost_price=30.00,
                current_stock=75,
                reorder_level=20,
                safety_stock=5,
                unit_of_measure='pieces'
            ),
        ]
        for product in products:
            db.session.add(product)
    
    db.session.commit()
    click.echo('Database initialized successfully!')

# Register CLI commands
app.cli.add_command(init_db)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
