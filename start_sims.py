#!/usr/bin/env python3
"""
Smart Inventory Management System (SIMS) - Quick Start Launcher
This script helps you get SIMS running quickly with minimal setup.
"""

import os
import sys
import subprocess
import webbrowser
from pathlib import Path

def print_banner():
    """Print SIMS banner"""
    print("=" * 60)
    print("🎯 Smart Inventory Management System (SIMS)")
    print("💡 Built for Moroccan Small Businesses")
    print("=" * 60)
    print()

def check_python():
    """Check Python version"""
    print("🔍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ required. Current version:", sys.version)
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    
    # Basic dependencies that are usually available
    basic_deps = [
        'flask==2.3.3',
        'flask-sqlalchemy==3.0.5',
        'werkzeug==2.3.7'
    ]
    
    try:
        for dep in basic_deps:
            print(f"Installing {dep}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', dep], 
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("✅ Basic dependencies installed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        print("💡 Try running: pip install flask flask-sqlalchemy")
        return False

def create_minimal_app():
    """Create a minimal version of the app for demo"""
    print("\n🏗️ Setting up minimal demo version...")
    
    # Create a simple demo app
    demo_app = '''
import os
from flask import Flask, render_template_string, jsonify
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'demo-secret-key'

# Sample data for demo
SAMPLE_PRODUCTS = [
    {
        'id': 1, 'name': 'Cotton Fabric - Blue', 'sku': 'CTN-BLU-001',
        'category': 'Textiles', 'current_stock': 150, 'reorder_level': 30,
        'unit_price': 25.50, 'cost_price': 18.00, 'status': 'Normal'
    },
    {
        'id': 2, 'name': 'LED Light Bulb 10W', 'sku': 'LED-10W-001', 
        'category': 'Electronics', 'current_stock': 5, 'reorder_level': 20,
        'unit_price': 45.00, 'cost_price': 30.00, 'status': 'Low Stock'
    },
    {
        'id': 3, 'name': 'Office Chair', 'sku': 'CHR-OFF-001',
        'category': 'Office Supplies', 'current_stock': 0, 'reorder_level': 5,
        'unit_price': 350.00, 'cost_price': 250.00, 'status': 'Out of Stock'
    }
]

DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SIMS - Smart Inventory Management System</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        body { background-color: #f8f9fa; }
        .card { border: none; box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075); }
        .navbar-brand { font-weight: 600; }
        .metric-card { transition: transform 0.2s; }
        .metric-card:hover { transform: translateY(-2px); }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container-fluid">
            <a class="navbar-brand" href="#">
                <i class="fas fa-boxes"></i> SIMS - Smart Inventory Management
            </a>
            <span class="navbar-text text-light">
                <i class="fas fa-flag"></i> Made for Moroccan Businesses
            </span>
        </div>
    </nav>

    <div class="container-fluid py-4">
        <div class="row mb-4">
            <div class="col-12">
                <h1 class="mb-4">
                    <i class="fas fa-tachometer-alt"></i> Dashboard
                    <small class="text-muted">Live Demo</small>
                </h1>
            </div>
        </div>

        <!-- Key Metrics -->
        <div class="row mb-4">
            <div class="col-md-3">
                <div class="card bg-primary text-white metric-card">
                    <div class="card-body">
                        <div class="d-flex justify-content-between">
                            <div>
                                <h4>{{ total_products }}</h4>
                                <p class="mb-0">Total Products</p>
                            </div>
                            <div class="align-self-center">
                                <i class="fas fa-box fa-2x"></i>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card bg-success text-white metric-card">
                    <div class="card-body">
                        <div class="d-flex justify-content-between">
                            <div>
                                <h4>{{ inventory_value }} MAD</h4>
                                <p class="mb-0">Inventory Value</p>
                            </div>
                            <div class="align-self-center">
                                <i class="fas fa-coins fa-2x"></i>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card bg-info text-white metric-card">
                    <div class="card-body">
                        <div class="d-flex justify-content-between">
                            <div>
                                <h4>{{ recent_sales }}</h4>
                                <p class="mb-0">Sales (7 days)</p>
                            </div>
                            <div class="align-self-center">
                                <i class="fas fa-shopping-cart fa-2x"></i>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card bg-warning text-dark metric-card">
                    <div class="card-body">
                        <div class="d-flex justify-content-between">
                            <div>
                                <h4>{{ low_stock_count }}</h4>
                                <p class="mb-0">Low Stock Items</p>
                            </div>
                            <div class="align-self-center">
                                <i class="fas fa-exclamation-triangle fa-2x"></i>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Products Table -->
        <div class="row">
            <div class="col-12">
                <div class="card">
                    <div class="card-header">
                        <h5 class="mb-0">
                            <i class="fas fa-box"></i> Product Inventory
                        </h5>
                    </div>
                    <div class="card-body">
                        <div class="table-responsive">
                            <table class="table table-hover">
                                <thead>
                                    <tr>
                                        <th>Product</th>
                                        <th>Category</th>
                                        <th>Stock</th>
                                        <th>Price</th>
                                        <th>Value</th>
                                        <th>Status</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {% for product in products %}
                                    <tr>
                                        <td>
                                            <strong>{{ product.name }}</strong><br>
                                            <small class="text-muted"><code>{{ product.sku }}</code></small>
                                        </td>
                                        <td><span class="badge bg-secondary">{{ product.category }}</span></td>
                                        <td>
                                            <strong>{{ product.current_stock }}</strong><br>
                                            <small class="text-muted">Reorder: {{ product.reorder_level }}</small>
                                        </td>
                                        <td>
                                            <strong>{{ "%.2f"|format(product.unit_price) }} MAD</strong><br>
                                            <small class="text-muted">Cost: {{ "%.2f"|format(product.cost_price) }}</small>
                                        </td>
                                        <td>
                                            <strong>{{ "%.2f"|format(product.current_stock * product.cost_price) }} MAD</strong>
                                        </td>
                                        <td>
                                            {% if product.status == 'Out of Stock' %}
                                                <span class="badge bg-dark">{{ product.status }}</span>
                                            {% elif product.status == 'Low Stock' %}
                                                <span class="badge bg-warning text-dark">{{ product.status }}</span>
                                            {% else %}
                                                <span class="badge bg-success">{{ product.status }}</span>
                                            {% endif %}
                                        </td>
                                    </tr>
                                    {% endfor %}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Features Demo -->
        <div class="row mt-4">
            <div class="col-12">
                <div class="card">
                    <div class="card-header">
                        <h5 class="mb-0">
                            <i class="fas fa-star"></i> SIMS Features
                        </h5>
                    </div>
                    <div class="card-body">
                        <div class="row">
                            <div class="col-md-4">
                                <h6><i class="fas fa-chart-line text-primary"></i> Analytics & Forecasting</h6>
                                <ul class="list-unstyled">
                                    <li>• Demand forecasting with ML</li>
                                    <li>• ABC analysis</li>
                                    <li>• Sales reports</li>
                                    <li>• Inventory optimization</li>
                                </ul>
                            </div>
                            <div class="col-md-4">
                                <h6><i class="fas fa-cogs text-success"></i> Smart Inventory</h6>
                                <ul class="list-unstyled">
                                    <li>• EOQ calculations</li>
                                    <li>• Automated reorder alerts</li>
                                    <li>• Stock level optimization</li>
                                    <li>• Supplier performance</li>
                                </ul>
                            </div>
                            <div class="col-md-4">
                                <h6><i class="fas fa-mobile-alt text-info"></i> Modern Interface</h6>
                                <ul class="list-unstyled">
                                    <li>• Responsive design</li>
                                    <li>• Real-time updates</li>
                                    <li>• RESTful API</li>
                                    <li>• Export capabilities</li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

@app.route('/')
def dashboard():
    # Calculate metrics
    total_products = len(SAMPLE_PRODUCTS)
    inventory_value = sum(p['current_stock'] * p['cost_price'] for p in SAMPLE_PRODUCTS)
    low_stock_count = sum(1 for p in SAMPLE_PRODUCTS if p['current_stock'] <= p['reorder_level'])
    recent_sales = 15  # Demo value
    
    return render_template_string(DASHBOARD_TEMPLATE, 
                                products=SAMPLE_PRODUCTS,
                                total_products=total_products,
                                inventory_value=f"{inventory_value:,.2f}",
                                low_stock_count=low_stock_count,
                                recent_sales=recent_sales)

@app.route('/api/dashboard')
def api_dashboard():
    return jsonify({
        'total_products': len(SAMPLE_PRODUCTS),
        'inventory_value': sum(p['current_stock'] * p['cost_price'] for p in SAMPLE_PRODUCTS),
        'low_stock_count': sum(1 for p in SAMPLE_PRODUCTS if p['current_stock'] <= p['reorder_level']),
        'status': 'demo'
    })

if __name__ == '__main__':
    print("🚀 Starting SIMS Demo...")
    print("📱 Open your browser to: http://localhost:5000")
    print("⏹️  Press Ctrl+C to stop")
    app.run(debug=True, host='0.0.0.0', port=5000)
'''
    
    with open('demo_app.py', 'w', encoding='utf-8') as f:
        f.write(demo_app)
    
    print("✅ Demo app created")
    return True

def main():
    """Main launcher function"""
    print_banner()
    
    # Check Python
    if not check_python():
        input("Press Enter to exit...")
        return
    
    # Try to install basic dependencies
    deps_ok = install_dependencies()
    
    if not deps_ok:
        print("\n🎯 Creating minimal demo version...")
        create_minimal_app()
        print("\n" + "="*60)
        print("🚀 QUICK START INSTRUCTIONS:")
        print("="*60)
        print("1. Install Flask: pip install flask")
        print("2. Run demo: python demo_app.py")
        print("3. Open browser: http://localhost:5000")
        print("="*60)
        input("Press Enter to exit...")
        return
    
    # Try to run the full application
    print("\n🚀 Starting SIMS application...")
    try:
        # Initialize database
        print("📊 Initializing database...")
        subprocess.run([sys.executable, 'run.py', 'init-db'], check=True)
        
        print("✅ Database initialized with sample data!")
        print("\n" + "="*60)
        print("🎉 SIMS IS READY!")
        print("="*60)
        print("🌐 Opening browser to: http://localhost:5000")
        print("⏹️  Press Ctrl+C in terminal to stop")
        print("="*60)
        
        # Open browser
        webbrowser.open('http://localhost:5000')
        
        # Start the application
        subprocess.run([sys.executable, 'run.py'])
        
    except Exception as e:
        print(f"❌ Error starting full application: {e}")
        print("\n🎯 Falling back to demo version...")
        create_minimal_app()
        print("\nRun: python demo_app.py")

if __name__ == '__main__':
    main()
