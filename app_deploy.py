#!/usr/bin/env python3
"""
SIMS - Smart Inventory Management System
Deployment-ready Flask Application

© 2024 Mustapha Baroudi. All Rights Reserved.
Contact: +212 697 362 759 | mustaphabaroudi833@gmail.com
LinkedIn: https://www.linkedin.com/in/baroudi-mustapha-2a257a289/
"""

import os
from flask import Flask, render_template_string, jsonify, request
from datetime import datetime, timedelta
import json
import random
import math

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'sims-mustapha-baroudi-2024')

# Sample data for the demo
products = [
    {
        'id': 1, 
        'name': 'Cotton Fabric - Blue', 
        'sku': 'CTN-BLU-001', 
        'category': 'Textiles', 
        'stock': 150, 
        'price': 25.50, 
        'cost': 18.00, 
        'status': 'Normal'
    },
    {
        'id': 2, 
        'name': 'LED Light Bulb 10W', 
        'sku': 'LED-10W-001', 
        'category': 'Electronics', 
        'stock': 5, 
        'price': 45.00, 
        'cost': 30.00, 
        'status': 'Low Stock'
    },
    {
        'id': 3, 
        'name': 'Office Chair Premium', 
        'sku': 'CHR-OFF-001', 
        'category': 'Office Supplies', 
        'stock': 0, 
        'price': 350.00, 
        'cost': 250.00, 
        'status': 'Out of Stock'
    },
    {
        'id': 4, 
        'name': 'Silk Fabric - Red', 
        'sku': 'SLK-RED-001', 
        'category': 'Textiles', 
        'stock': 75, 
        'price': 85.00, 
        'cost': 60.00, 
        'status': 'Normal'
    },
    {
        'id': 5, 
        'name': 'Wireless Mouse', 
        'sku': 'MSE-WRL-001', 
        'category': 'Electronics', 
        'stock': 8, 
        'price': 120.00, 
        'cost': 80.00, 
        'status': 'Low Stock'
    }
]

# Sales data
sales = []
next_sale_id = 1

@app.route('/')
def index():
    """Main application route - serves the interactive demo"""
    return render_template_string(MAIN_TEMPLATE)

@app.route('/api/products')
def get_products():
    """API endpoint to get all products"""
    return jsonify(products)

@app.route('/api/products', methods=['POST'])
def add_product():
    """API endpoint to add a new product"""
    global products
    data = request.json
    
    new_product = {
        'id': len(products) + 1,
        'name': data.get('name'),
        'sku': data.get('sku'),
        'category': data.get('category'),
        'stock': int(data.get('stock', 0)),
        'price': float(data.get('price')),
        'cost': float(data.get('cost')),
        'status': 'Normal' if int(data.get('stock', 0)) > 10 else 'Low Stock' if int(data.get('stock', 0)) > 0 else 'Out of Stock'
    }
    
    products.append(new_product)
    return jsonify({'success': True, 'product': new_product})

@app.route('/api/products/<int:product_id>/stock', methods=['PUT'])
def update_stock(product_id):
    """API endpoint to update product stock"""
    global products
    data = request.json
    adjustment = int(data.get('adjustment', 0))
    
    for product in products:
        if product['id'] == product_id:
            product['stock'] = max(0, product['stock'] + adjustment)
            # Update status
            if product['stock'] == 0:
                product['status'] = 'Out of Stock'
            elif product['stock'] <= 10:
                product['status'] = 'Low Stock'
            else:
                product['status'] = 'Normal'
            
            return jsonify({'success': True, 'product': product})
    
    return jsonify({'success': False, 'error': 'Product not found'}), 404

@app.route('/api/sales', methods=['POST'])
def process_sale():
    """API endpoint to process a sale"""
    global products, sales, next_sale_id
    data = request.json
    
    sale_items = data.get('items', [])
    customer_name = data.get('customer_name', 'Walk-in Customer')
    
    # Update product stocks
    total_amount = 0
    for item in sale_items:
        product_id = item['product_id']
        quantity = item['quantity']
        
        for product in products:
            if product['id'] == product_id:
                if product['stock'] >= quantity:
                    product['stock'] -= quantity
                    total_amount += quantity * product['price']
                    
                    # Update status
                    if product['stock'] == 0:
                        product['status'] = 'Out of Stock'
                    elif product['stock'] <= 10:
                        product['status'] = 'Low Stock'
                    else:
                        product['status'] = 'Normal'
                else:
                    return jsonify({'success': False, 'error': f'Insufficient stock for {product["name"]}'}), 400
    
    # Create sale record
    sale = {
        'id': next_sale_id,
        'sale_number': f'#{datetime.now().strftime("%Y%m%d")}{next_sale_id:03d}',
        'customer_name': customer_name,
        'items': sale_items,
        'total_amount': total_amount,
        'tax_amount': total_amount * 0.2,  # 20% VAT
        'final_amount': total_amount * 1.2,
        'date': datetime.now().isoformat(),
        'status': 'Paid'
    }
    
    sales.append(sale)
    next_sale_id += 1
    
    return jsonify({'success': True, 'sale': sale})

@app.route('/api/forecast/<category>')
def get_forecast_data(category):
    """API endpoint to get demand forecast data"""
    # Generate realistic forecast data
    today = datetime.now()
    labels = []
    historical_data = []
    forecast_data = []
    confidence_upper = []
    confidence_lower = []

    # Generate last 30 days (historical)
    for i in range(29, -1, -1):
        date = today - timedelta(days=i)
        labels.append(date.strftime('%b %d'))
        
        # Generate realistic historical data with seasonality
        base_value = 150 if category == 'textiles' else 80 if category == 'electronics' else 120
        seasonality = math.sin((i / 30) * math.pi * 2) * 20
        random_variation = (random.random() - 0.5) * 30
        weekend_effect = -15 if date.weekday() >= 5 else 0
        
        historical_data.append(max(0, base_value + seasonality + random_variation + weekend_effect))

    # Generate next 30 days (forecast)
    for i in range(1, 31):
        date = today + timedelta(days=i)
        labels.append(date.strftime('%b %d'))
        
        # Generate forecast with trend
        last_historical = historical_data[-1]
        trend = 1.02 if category == 'textiles' else 1.05 if category == 'electronics' else 1.03
        base_value = last_historical * (trend ** (i / 30))
        seasonality = math.sin(((30 + i) / 30) * math.pi * 2) * 15
        random_variation = (random.random() - 0.5) * 10
        
        forecast_value = max(0, base_value + seasonality + random_variation)
        forecast_data.append(forecast_value)
        
        # Confidence intervals
        confidence_width = 10 + (i / 30) * 20
        confidence_upper.append(forecast_value + confidence_width)
        confidence_lower.append(max(0, forecast_value - confidence_width))

    return jsonify({
        'labels': labels,
        'historical': historical_data,
        'forecast': forecast_data,
        'confidence_upper': confidence_upper,
        'confidence_lower': confidence_lower
    })

@app.route('/health')
def health_check():
    """Health check endpoint for deployment platforms"""
    return jsonify({
        'status': 'healthy',
        'app': 'SIMS - Smart Inventory Management System',
        'developer': 'Mustapha Baroudi',
        'contact': '+212 697 362 759',
        'email': 'mustaphabaroudi833@gmail.com',
        'linkedin': 'https://www.linkedin.com/in/baroudi-mustapha-2a257a289/',
        'timestamp': datetime.now().isoformat()
    })

# HTML Template (will be moved to separate file for production)
MAIN_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SIMS - Smart Inventory Management System | Mustapha Baroudi</title>
    <meta name="description" content="Professional inventory management system by Mustapha Baroudi - Full-Stack Developer from Morocco">
    <meta name="author" content="Mustapha Baroudi">
    <meta name="keywords" content="inventory management, Morocco, web development, Mustapha Baroudi">
    
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    
    <style>
        :root {
            --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            --success-gradient: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            --warning-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            --info-gradient: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            --dark-gradient: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
        }

        * { transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); }
        
        body { 
            font-family: 'Inter', sans-serif;
            background: var(--primary-gradient);
            min-height: 100vh;
        }

        .main-container {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            border-radius: 20px;
            margin: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            animation: slideInUp 0.8s ease-out;
        }

        @keyframes slideInUp {
            from { transform: translateY(50px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }

        .navbar {
            background: rgba(255, 255, 255, 0.1) !important;
            backdrop-filter: blur(20px);
            border-bottom: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 20px 20px 0 0;
        }

        .navbar-brand { 
            font-weight: 700; 
            font-size: 1.5rem;
            background: var(--primary-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .card {
            border: none;
            border-radius: 20px;
            background: rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(10px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }

        .card:hover {
            transform: translateY(-10px) scale(1.02);
            box-shadow: 0 20px 40px rgba(0,0,0,0.15);
        }

        .metric-card {
            cursor: pointer;
            position: relative;
            overflow: hidden;
        }

        .metric-card.primary { background: var(--primary-gradient); }
        .metric-card.success { background: var(--success-gradient); }
        .metric-card.warning { background: var(--warning-gradient); }
        .metric-card.info { background: var(--info-gradient); }

        .btn {
            border-radius: 15px;
            font-weight: 500;
            padding: 12px 25px;
            border: none;
            transition: all 0.3s ease;
        }

        .btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 30px rgba(0,0,0,0.2);
        }

        .btn-primary { background: var(--primary-gradient); }
        .btn-success { background: var(--success-gradient); }
        .btn-warning { background: var(--warning-gradient); }
        .btn-info { background: var(--info-gradient); }

        .notification {
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 9999;
            min-width: 350px;
            border-radius: 15px;
            backdrop-filter: blur(20px);
            animation: slideInRight 0.5s ease-out;
        }

        @keyframes slideInRight {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }

        .demo-badge {
            position: fixed;
            top: 20px;
            left: 20px;
            z-index: 1000;
            animation: bounce 2s infinite;
        }

        @keyframes bounce {
            0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
            40% { transform: translateY(-10px); }
            60% { transform: translateY(-5px); }
        }

        footer {
            background: var(--dark-gradient);
            color: white;
            margin-top: 50px;
            padding: 30px 0;
        }

        .developer-info {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 20px;
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <div class="demo-badge">
        <span class="badge bg-success fs-6">
            <i class="fas fa-rocket"></i> LIVE DEMO
        </span>
    </div>

    <div class="main-container">
        <!-- Navigation -->
        <nav class="navbar navbar-expand-lg">
            <div class="container-fluid">
                <a class="navbar-brand" href="#">
                    <i class="fas fa-gem"></i> SIMS Pro
                </a>
                
                <div class="navbar-nav me-auto">
                    <span class="nav-link">
                        <i class="fas fa-tachometer-alt"></i> Live Dashboard
                    </span>
                </div>
                
                <div class="navbar-nav">
                    <span class="navbar-text text-dark fw-bold me-3">
                        <i class="fas fa-flag text-success"></i> Morocco 🇲🇦
                    </span>
                    <button class="btn btn-outline-primary btn-sm" onclick="showDeveloperInfo()">
                        <i class="fas fa-user-tie"></i> Developer
                    </button>
                </div>
            </div>
        </nav>

        <!-- Main Content -->
        <div class="container-fluid py-4">
            <div class="row mb-4">
                <div class="col-12 text-center">
                    <h1 class="fw-bold mb-3">
                        <i class="fas fa-rocket text-primary"></i> SIMS - Live Demo
                    </h1>
                    <p class="text-muted fs-5">Smart Inventory Management System</p>
                    <p class="text-muted">Professional web application accessible from anywhere in the world!</p>
                </div>
            </div>

            <!-- Metrics Cards -->
            <div class="row mb-5">
                <div class="col-md-3 mb-4">
                    <div class="card metric-card primary text-white" onclick="showInfo('products')">
                        <div class="card-body text-center">
                            <h2 class="fw-bold mb-1">5</h2>
                            <p class="mb-0 opacity-90">Total Products</p>
                            <small class="opacity-75">Active inventory</small>
                        </div>
                    </div>
                </div>
                <div class="col-md-3 mb-4">
                    <div class="card metric-card success text-white" onclick="showInfo('value')">
                        <div class="card-body text-center">
                            <h2 class="fw-bold mb-1">18,840 MAD</h2>
                            <p class="mb-0 opacity-90">Inventory Value</p>
                            <small class="opacity-75">Total worth</small>
                        </div>
                    </div>
                </div>
                <div class="col-md-3 mb-4">
                    <div class="card metric-card info text-white" onclick="showInfo('sales')">
                        <div class="card-body text-center">
                            <h2 class="fw-bold mb-1">23</h2>
                            <p class="mb-0 opacity-90">Sales (7 days)</p>
                            <small class="opacity-75">Recent activity</small>
                        </div>
                    </div>
                </div>
                <div class="col-md-3 mb-4">
                    <div class="card metric-card warning text-white" onclick="showInfo('alerts')">
                        <div class="card-body text-center">
                            <h2 class="fw-bold mb-1">2</h2>
                            <p class="mb-0 opacity-90">Low Stock</p>
                            <small class="opacity-75">Need attention</small>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Features Showcase -->
            <div class="row mb-5">
                <div class="col-12">
                    <div class="card">
                        <div class="card-header bg-transparent">
                            <h5 class="fw-bold mb-0">
                                <i class="fas fa-star text-warning"></i> Live System Features
                            </h5>
                        </div>
                        <div class="card-body">
                            <div class="row">
                                <div class="col-md-3 mb-3">
                                    <div class="text-center p-3 rounded" style="background: rgba(102, 126, 234, 0.1);">
                                        <i class="fas fa-chart-line text-primary fs-1 mb-3"></i>
                                        <h6 class="fw-bold">Real-time Analytics</h6>
                                        <p class="text-muted small">Live business metrics and forecasting</p>
                                    </div>
                                </div>
                                <div class="col-md-3 mb-3">
                                    <div class="text-center p-3 rounded" style="background: rgba(40, 167, 69, 0.1);">
                                        <i class="fas fa-shopping-cart text-success fs-1 mb-3"></i>
                                        <h6 class="fw-bold">Point of Sale</h6>
                                        <p class="text-muted small">Complete sales transaction system</p>
                                    </div>
                                </div>
                                <div class="col-md-3 mb-3">
                                    <div class="text-center p-3 rounded" style="background: rgba(255, 193, 7, 0.1);">
                                        <i class="fas fa-boxes text-warning fs-1 mb-3"></i>
                                        <h6 class="fw-bold">Inventory Control</h6>
                                        <p class="text-muted small">Smart stock management and alerts</p>
                                    </div>
                                </div>
                                <div class="col-md-3 mb-3">
                                    <div class="text-center p-3 rounded" style="background: rgba(220, 53, 69, 0.1);">
                                        <i class="fas fa-mobile-alt text-danger fs-1 mb-3"></i>
                                        <h6 class="fw-bold">Mobile Ready</h6>
                                        <p class="text-muted small">Works perfectly on all devices</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Call to Action -->
            <div class="row">
                <div class="col-12">
                    <div class="card text-center" style="background: var(--primary-gradient); color: white;">
                        <div class="card-body py-5">
                            <h3 class="fw-bold mb-3">
                                <i class="fas fa-globe"></i> Accessible Worldwide!
                            </h3>
                            <p class="fs-5 mb-4">
                                This professional inventory management system is now live and accessible from anywhere in the world.
                                Perfect for showcasing on LinkedIn and professional portfolios!
                            </p>
                            <div class="row justify-content-center">
                                <div class="col-md-8">
                                    <div class="row">
                                        <div class="col-md-4 mb-3">
                                            <button class="btn btn-light w-100" onclick="showDeveloperInfo()">
                                                <i class="fas fa-user-tie"></i><br>
                                                <strong>Meet Developer</strong>
                                            </button>
                                        </div>
                                        <div class="col-md-4 mb-3">
                                            <a href="https://www.linkedin.com/in/baroudi-mustapha-2a257a289/" 
                                               target="_blank" class="btn btn-light w-100">
                                                <i class="fab fa-linkedin"></i><br>
                                                <strong>LinkedIn Profile</strong>
                                            </a>
                                        </div>
                                        <div class="col-md-4 mb-3">
                                            <a href="tel:+212697362759" class="btn btn-light w-100">
                                                <i class="fas fa-phone"></i><br>
                                                <strong>Contact Now</strong>
                                            </a>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Professional Footer -->
        <footer>
            <div class="container-fluid">
                <div class="row align-items-center">
                    <div class="col-md-6">
                        <div class="d-flex align-items-center mb-3 mb-md-0">
                            <div class="me-4">
                                <img src="https://via.placeholder.com/60x60/667eea/ffffff?text=MB" 
                                     alt="Mustapha Baroudi" class="rounded-circle" 
                                     style="border: 3px solid rgba(255,255,255,0.2);">
                            </div>
                            <div>
                                <h6 class="fw-bold mb-1">
                                    <i class="fas fa-code text-warning"></i> Developed by Mustapha Baroudi
                                </h6>
                                <p class="mb-0 opacity-75">Full-Stack Developer & Software Engineer</p>
                                <small class="opacity-50">© 2024 All Rights Reserved</small>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="row text-center text-md-end">
                            <div class="col-12">
                                <div class="d-flex justify-content-center justify-content-md-end gap-3 mb-2">
                                    <a href="tel:+212697362759" class="text-white text-decoration-none">
                                        <i class="fas fa-phone-alt"></i> +212 697 362 759
                                    </a>
                                    <a href="mailto:mustaphabaroudi833@gmail.com" class="text-white text-decoration-none">
                                        <i class="fas fa-envelope"></i> Email
                                    </a>
                                    <a href="https://www.linkedin.com/in/baroudi-mustapha-2a257a289/" 
                                       target="_blank" class="text-white text-decoration-none">
                                        <i class="fab fa-linkedin"></i> LinkedIn
                                    </a>
                                </div>
                                <small class="opacity-75">
                                    <i class="fas fa-heart text-danger"></i> 
                                    Built with passion for Moroccan businesses
                                </small>
                            </div>
                        </div>
                    </div>
                </div>
                <hr class="my-3 opacity-25">
                <div class="row">
                    <div class="col-12 text-center">
                        <small class="opacity-50">
                            SIMS (Smart Inventory Management System) - Professional Portfolio Project<br>
                            Showcasing advanced full-stack development skills with modern web technologies
                        </small>
                    </div>
                </div>
            </div>
        </footer>
    </div>

    <!-- Developer Modal -->
    <div class="modal fade" id="developerModal" tabindex="-1">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header" style="background: var(--primary-gradient); color: white;">
                    <h5 class="modal-title fw-bold">
                        <i class="fas fa-user-tie"></i> Meet the Developer
                    </h5>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <div class="row">
                        <div class="col-md-4 text-center mb-4">
                            <img src="https://via.placeholder.com/150x150/667eea/ffffff?text=MB" 
                                 alt="Mustapha Baroudi" class="rounded-circle mb-3" 
                                 style="width: 150px; height: 150px; border: 5px solid var(--primary-gradient);">
                            <h4 class="fw-bold">Mustapha Baroudi</h4>
                            <p class="text-muted">Full-Stack Developer</p>
                            <div class="d-flex justify-content-center gap-2">
                                <span class="badge bg-primary">Python</span>
                                <span class="badge bg-success">JavaScript</span>
                                <span class="badge bg-info">Flask</span>
                                <span class="badge bg-warning text-dark">React</span>
                            </div>
                        </div>
                        <div class="col-md-8">
                            <h5 class="fw-bold mb-3">
                                <i class="fas fa-briefcase text-primary"></i> About This Project
                            </h5>
                            <p class="mb-3">
                                SIMS is now a live web application accessible from anywhere in the world! 
                                This demonstrates advanced full-stack development skills including:
                            </p>
                            <div class="row mb-4">
                                <div class="col-md-6">
                                    <ul class="list-unstyled">
                                        <li><i class="fas fa-check text-success"></i> Flask Web Development</li>
                                        <li><i class="fas fa-check text-success"></i> RESTful API Design</li>
                                        <li><i class="fas fa-check text-success"></i> Cloud Deployment</li>
                                        <li><i class="fas fa-check text-success"></i> Interactive UI/UX</li>
                                    </ul>
                                </div>
                                <div class="col-md-6">
                                    <ul class="list-unstyled">
                                        <li><i class="fas fa-check text-success"></i> Real-time Data Processing</li>
                                        <li><i class="fas fa-check text-success"></i> Responsive Design</li>
                                        <li><i class="fas fa-check text-success"></i> Professional Deployment</li>
                                        <li><i class="fas fa-check text-success"></i> Global Accessibility</li>
                                    </ul>
                                </div>
                            </div>
                            
                            <div class="developer-info">
                                <h6 class="fw-bold mb-3">
                                    <i class="fas fa-handshake text-success"></i> Let's Connect & Collaborate
                                </h6>
                                <p class="mb-3">
                                    Available for custom software development, web applications, 
                                    and technical consulting projects.
                                </p>
                                
                                <div class="row">
                                    <div class="col-md-4 mb-3">
                                        <div class="text-center">
                                            <i class="fas fa-phone-alt text-primary fs-3 mb-2"></i>
                                            <h6 class="fw-bold">Call Me</h6>
                                            <a href="tel:+212697362759" class="text-decoration-none">
                                                +212 697 362 759
                                            </a>
                                        </div>
                                    </div>
                                    <div class="col-md-4 mb-3">
                                        <div class="text-center">
                                            <i class="fas fa-envelope text-success fs-3 mb-2"></i>
                                            <h6 class="fw-bold">Email Me</h6>
                                            <a href="mailto:mustaphabaroudi833@gmail.com" class="text-decoration-none">
                                                mustaphabaroudi833@gmail.com
                                            </a>
                                        </div>
                                    </div>
                                    <div class="col-md-4 mb-3">
                                        <div class="text-center">
                                            <i class="fab fa-linkedin text-info fs-3 mb-2"></i>
                                            <h6 class="fw-bold">LinkedIn</h6>
                                            <a href="https://www.linkedin.com/in/baroudi-mustapha-2a257a289/" 
                                               target="_blank" class="text-decoration-none">
                                                Professional Profile
                                            </a>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    <a href="https://www.linkedin.com/in/baroudi-mustapha-2a257a289/" 
                       target="_blank" class="btn btn-primary">
                        <i class="fab fa-linkedin"></i> View LinkedIn Profile
                    </a>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        function showDeveloperInfo() {
            new bootstrap.Modal(document.getElementById('developerModal')).show();
        }

        function showInfo(type) {
            const messages = {
                products: 'Total Products: 5 active products across multiple categories including textiles, electronics, and office supplies.',
                value: 'Inventory Value: 18,840.00 MAD total inventory worth with detailed cost and retail value tracking.',
                sales: 'Recent Sales: 23 transactions in the last 7 days with comprehensive sales analytics.',
                alerts: 'Low Stock Alerts: 2 products need immediate attention for reordering.'
            };
            
            showNotification('System Info', messages[type], 'info');
        }

        function showNotification(title, message, type = 'info') {
            const notification = document.createElement('div');
            notification.className = `notification alert alert-${type} alert-dismissible fade show`;
            notification.innerHTML = `
                <div class="d-flex align-items-center">
                    <div class="me-3">
                        <i class="fas fa-info-circle fs-4"></i>
                    </div>
                    <div class="flex-grow-1">
                        <h6 class="fw-bold mb-1">${title}</h6>
                        <p class="mb-0">${message}</p>
                    </div>
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                </div>
            `;
            document.body.appendChild(notification);
            
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.style.transform = 'translateX(100%)';
                    notification.style.opacity = '0';
                    setTimeout(() => notification.remove(), 300);
                }
            }, 5000);
        }

        // Welcome message
        document.addEventListener('DOMContentLoaded', function() {
            setTimeout(() => {
                showNotification('Welcome to SIMS!', 
                    'This is a live web application accessible from anywhere in the world! Perfect for LinkedIn portfolio showcase.', 
                    'success');
            }, 1000);
        });
    </script>
</body>
</html>
'''

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
