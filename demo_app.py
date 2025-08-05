#!/usr/bin/env python3
"""
SIMS Demo - Simplified version to showcase the system
"""

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
        'id': 3, 'name': 'Office Chair Premium', 'sku': 'CHR-OFF-001',
        'category': 'Office Supplies', 'current_stock': 0, 'reorder_level': 5,
        'unit_price': 350.00, 'cost_price': 250.00, 'status': 'Out of Stock'
    },
    {
        'id': 4, 'name': 'Silk Fabric - Red', 'sku': 'SLK-RED-001',
        'category': 'Textiles', 'current_stock': 75, 'reorder_level': 15,
        'unit_price': 85.00, 'cost_price': 60.00, 'status': 'Normal'
    },
    {
        'id': 5, 'name': 'Wireless Mouse', 'sku': 'MSE-WRL-001',
        'category': 'Electronics', 'current_stock': 8, 'reorder_level': 12,
        'unit_price': 120.00, 'cost_price': 80.00, 'status': 'Low Stock'
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
        .card { 
            border: none; 
            box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
            transition: box-shadow 0.15s ease-in-out;
        }
        .card:hover { box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15); }
        .navbar-brand { font-weight: 600; }
        .metric-card { transition: transform 0.2s; }
        .metric-card:hover { transform: translateY(-2px); }
        .demo-badge { 
            position: fixed; 
            top: 70px; 
            right: 20px; 
            z-index: 1000;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.7; }
            100% { opacity: 1; }
        }
        .feature-icon { font-size: 2rem; margin-bottom: 1rem; }
    </style>
</head>
<body>
    <div class="demo-badge">
        <span class="badge bg-danger fs-6">
            <i class="fas fa-play"></i> LIVE DEMO
        </span>
    </div>

    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container-fluid">
            <a class="navbar-brand" href="#">
                <i class="fas fa-boxes"></i> SIMS - Smart Inventory Management
            </a>
            <div class="navbar-nav ms-auto">
                <span class="navbar-text text-light">
                    <i class="fas fa-flag"></i> Made for Moroccan Businesses 🇲🇦
                </span>
            </div>
        </div>
    </nav>

    <div class="container-fluid py-4">
        <!-- Header -->
        <div class="row mb-4">
            <div class="col-12">
                <div class="d-flex justify-content-between align-items-center">
                    <div>
                        <h1 class="mb-2">
                            <i class="fas fa-tachometer-alt text-primary"></i> Dashboard
                        </h1>
                        <p class="text-muted mb-0">Real-time inventory overview and analytics</p>
                    </div>
                    <div>
                        <span class="badge bg-success fs-6">
                            <i class="fas fa-circle"></i> System Online
                        </span>
                    </div>
                </div>
            </div>
        </div>

        <!-- Key Metrics -->
        <div class="row mb-4">
            <div class="col-md-3 mb-3">
                <div class="card bg-primary text-white metric-card">
                    <div class="card-body">
                        <div class="d-flex justify-content-between">
                            <div>
                                <h3 class="mb-1">{{ total_products }}</h3>
                                <p class="mb-0">Total Products</p>
                                <small class="opacity-75">Active inventory items</small>
                            </div>
                            <div class="align-self-center">
                                <i class="fas fa-box fa-3x opacity-75"></i>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-3 mb-3">
                <div class="card bg-success text-white metric-card">
                    <div class="card-body">
                        <div class="d-flex justify-content-between">
                            <div>
                                <h3 class="mb-1">{{ inventory_value }} MAD</h3>
                                <p class="mb-0">Inventory Value</p>
                                <small class="opacity-75">Total stock worth</small>
                            </div>
                            <div class="align-self-center">
                                <i class="fas fa-coins fa-3x opacity-75"></i>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-3 mb-3">
                <div class="card bg-info text-white metric-card">
                    <div class="card-body">
                        <div class="d-flex justify-content-between">
                            <div>
                                <h3 class="mb-1">{{ recent_sales }}</h3>
                                <p class="mb-0">Sales (7 days)</p>
                                <small class="opacity-75">Recent transactions</small>
                            </div>
                            <div class="align-self-center">
                                <i class="fas fa-shopping-cart fa-3x opacity-75"></i>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-3 mb-3">
                <div class="card bg-warning text-dark metric-card">
                    <div class="card-body">
                        <div class="d-flex justify-content-between">
                            <div>
                                <h3 class="mb-1">{{ low_stock_count }}</h3>
                                <p class="mb-0">Low Stock Items</p>
                                <small class="opacity-75">Need attention</small>
                            </div>
                            <div class="align-self-center">
                                <i class="fas fa-exclamation-triangle fa-3x opacity-75"></i>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Products Table -->
        <div class="row mb-4">
            <div class="col-12">
                <div class="card">
                    <div class="card-header bg-white">
                        <div class="d-flex justify-content-between align-items-center">
                            <h5 class="mb-0">
                                <i class="fas fa-warehouse text-primary"></i> Product Inventory
                            </h5>
                            <div>
                                <span class="badge bg-light text-dark">{{ total_products }} items</span>
                            </div>
                        </div>
                    </div>
                    <div class="card-body p-0">
                        <div class="table-responsive">
                            <table class="table table-hover mb-0">
                                <thead class="table-light">
                                    <tr>
                                        <th class="border-0">Product</th>
                                        <th class="border-0">Category</th>
                                        <th class="border-0">Stock Level</th>
                                        <th class="border-0">Pricing</th>
                                        <th class="border-0">Value</th>
                                        <th class="border-0">Status</th>
                                        <th class="border-0">Actions</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {% for product in products %}
                                    <tr>
                                        <td class="py-3">
                                            <div>
                                                <strong class="d-block">{{ product.name }}</strong>
                                                <small class="text-muted">
                                                    <i class="fas fa-barcode"></i> {{ product.sku }}
                                                </small>
                                            </div>
                                        </td>
                                        <td class="py-3">
                                            <span class="badge bg-secondary">{{ product.category }}</span>
                                        </td>
                                        <td class="py-3">
                                            <div>
                                                <strong class="d-block">{{ product.current_stock }} units</strong>
                                                <small class="text-muted">Reorder at: {{ product.reorder_level }}</small>
                                            </div>
                                        </td>
                                        <td class="py-3">
                                            <div>
                                                <strong class="d-block text-success">{{ "%.2f"|format(product.unit_price) }} MAD</strong>
                                                <small class="text-muted">Cost: {{ "%.2f"|format(product.cost_price) }} MAD</small>
                                            </div>
                                        </td>
                                        <td class="py-3">
                                            <strong class="text-primary">{{ "%.2f"|format(product.current_stock * product.cost_price) }} MAD</strong>
                                        </td>
                                        <td class="py-3">
                                            {% if product.status == 'Out of Stock' %}
                                                <span class="badge bg-dark">
                                                    <i class="fas fa-times"></i> {{ product.status }}
                                                </span>
                                            {% elif product.status == 'Low Stock' %}
                                                <span class="badge bg-warning text-dark">
                                                    <i class="fas fa-exclamation-triangle"></i> {{ product.status }}
                                                </span>
                                            {% else %}
                                                <span class="badge bg-success">
                                                    <i class="fas fa-check"></i> {{ product.status }}
                                                </span>
                                            {% endif %}
                                        </td>
                                        <td class="py-3">
                                            <div class="btn-group btn-group-sm">
                                                <button class="btn btn-outline-primary" title="View Details">
                                                    <i class="fas fa-eye"></i>
                                                </button>
                                                <button class="btn btn-outline-secondary" title="Edit">
                                                    <i class="fas fa-edit"></i>
                                                </button>
                                                <button class="btn btn-outline-info" title="Adjust Stock">
                                                    <i class="fas fa-boxes"></i>
                                                </button>
                                            </div>
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

        <!-- Features Showcase -->
        <div class="row">
            <div class="col-12">
                <div class="card">
                    <div class="card-header bg-white">
                        <h5 class="mb-0">
                            <i class="fas fa-star text-warning"></i> SIMS Features & Capabilities
                        </h5>
                    </div>
                    <div class="card-body">
                        <div class="row">
                            <div class="col-md-4 text-center mb-4">
                                <div class="feature-icon text-primary">
                                    <i class="fas fa-chart-line"></i>
                                </div>
                                <h6 class="fw-bold">Advanced Analytics</h6>
                                <ul class="list-unstyled text-start">
                                    <li><i class="fas fa-check text-success"></i> Demand forecasting with ML</li>
                                    <li><i class="fas fa-check text-success"></i> ABC product analysis</li>
                                    <li><i class="fas fa-check text-success"></i> Sales trend reports</li>
                                    <li><i class="fas fa-check text-success"></i> Inventory optimization</li>
                                </ul>
                            </div>
                            <div class="col-md-4 text-center mb-4">
                                <div class="feature-icon text-success">
                                    <i class="fas fa-cogs"></i>
                                </div>
                                <h6 class="fw-bold">Smart Inventory</h6>
                                <ul class="list-unstyled text-start">
                                    <li><i class="fas fa-check text-success"></i> EOQ calculations</li>
                                    <li><i class="fas fa-check text-success"></i> Automated reorder alerts</li>
                                    <li><i class="fas fa-check text-success"></i> Stock level optimization</li>
                                    <li><i class="fas fa-check text-success"></i> Supplier performance tracking</li>
                                </ul>
                            </div>
                            <div class="col-md-4 text-center mb-4">
                                <div class="feature-icon text-info">
                                    <i class="fas fa-mobile-alt"></i>
                                </div>
                                <h6 class="fw-bold">Modern Interface</h6>
                                <ul class="list-unstyled text-start">
                                    <li><i class="fas fa-check text-success"></i> Responsive design</li>
                                    <li><i class="fas fa-check text-success"></i> Real-time updates</li>
                                    <li><i class="fas fa-check text-success"></i> RESTful API</li>
                                    <li><i class="fas fa-check text-success"></i> Export capabilities</li>
                                </ul>
                            </div>
                        </div>
                        
                        <div class="row mt-4">
                            <div class="col-12">
                                <div class="alert alert-info">
                                    <h6><i class="fas fa-info-circle"></i> About This Demo</h6>
                                    <p class="mb-2">This is a live demonstration of the Smart Inventory Management System (SIMS) built specifically for Moroccan small businesses. The full system includes:</p>
                                    <div class="row">
                                        <div class="col-md-6">
                                            <ul class="mb-0">
                                                <li>Complete product catalog management</li>
                                                <li>Sales transaction processing</li>
                                                <li>Inventory movement tracking</li>
                                                <li>Supplier relationship management</li>
                                            </ul>
                                        </div>
                                        <div class="col-md-6">
                                            <ul class="mb-0">
                                                <li>Advanced reporting and analytics</li>
                                                <li>Demand forecasting algorithms</li>
                                                <li>Multi-currency support (MAD focus)</li>
                                                <li>Export/import capabilities</li>
                                            </ul>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <footer class="bg-light text-center py-3 mt-5">
        <div class="container">
            <span class="text-muted">
                <i class="fas fa-heart text-danger"></i> 
                SIMS v1.0.0 - Built for Moroccan Small Businesses
                <i class="fas fa-flag text-success"></i>
            </span>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // Add some interactivity
        document.addEventListener('DOMContentLoaded', function() {
            // Animate counters
            const counters = document.querySelectorAll('.metric-card h3');
            counters.forEach(counter => {
                const target = parseInt(counter.textContent);
                let current = 0;
                const increment = target / 20;
                const timer = setInterval(() => {
                    current += increment;
                    if (current >= target) {
                        counter.textContent = target;
                        clearInterval(timer);
                    } else {
                        counter.textContent = Math.floor(current);
                    }
                }, 50);
            });
            
            // Add click handlers to demo buttons
            document.querySelectorAll('.btn').forEach(btn => {
                btn.addEventListener('click', function(e) {
                    e.preventDefault();
                    alert('This is a demo! In the full system, this would ' + this.title.toLowerCase() + '.');
                });
            });
        });
    </script>
</body>
</html>
"""

@app.route('/')
def dashboard():
    """Main dashboard route"""
    # Calculate metrics
    total_products = len(SAMPLE_PRODUCTS)
    inventory_value = sum(p['current_stock'] * p['cost_price'] for p in SAMPLE_PRODUCTS)
    low_stock_count = sum(1 for p in SAMPLE_PRODUCTS if p['current_stock'] <= p['reorder_level'])
    recent_sales = 23  # Demo value
    
    return render_template_string(DASHBOARD_TEMPLATE, 
                                products=SAMPLE_PRODUCTS,
                                total_products=total_products,
                                inventory_value=f"{inventory_value:,.2f}",
                                low_stock_count=low_stock_count,
                                recent_sales=recent_sales)

@app.route('/api/dashboard')
def api_dashboard():
    """API endpoint for dashboard data"""
    return jsonify({
        'total_products': len(SAMPLE_PRODUCTS),
        'inventory_value': sum(p['current_stock'] * p['cost_price'] for p in SAMPLE_PRODUCTS),
        'low_stock_count': sum(1 for p in SAMPLE_PRODUCTS if p['current_stock'] <= p['reorder_level']),
        'recent_sales': 23,
        'status': 'demo_active',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'version': '1.0.0-demo',
        'timestamp': datetime.now().isoformat(),
        'database': 'demo_data'
    })

if __name__ == '__main__':
    print("🚀 Starting SIMS Demo Application...")
    print("=" * 50)
    print("📱 Open your browser to: http://localhost:5000")
    print("🎯 This is a live demo of the full SIMS system")
    print("⏹️  Press Ctrl+C to stop the server")
    print("=" * 50)
    app.run(debug=True, host='0.0.0.0', port=5000)
