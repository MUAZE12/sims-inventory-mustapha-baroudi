#!/usr/bin/env python3
"""
SIMS - Smart Inventory Management System
Live Web Application

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

# HTML Template
MAIN_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SIMS - Smart Inventory Management | Mustapha Baroudi</title>
    <meta name="description" content="Professional inventory management system by Mustapha Baroudi - Full-Stack Developer from Morocco">
    <meta name="author" content="Mustapha Baroudi">
    
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    
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
    </style>
</head>
<body>
    <div class="demo-badge">
        <span class="badge bg-success fs-6">
            <i class="fas fa-globe"></i> LIVE WORLDWIDE
        </span>
    </div>

    <div class="main-container">
        <!-- Navigation -->
        <nav class="navbar navbar-expand-lg">
            <div class="container-fluid">
                <a class="navbar-brand" href="#">
                    <i class="fas fa-gem"></i> SIMS Live
                </a>
                
                <div class="navbar-nav me-auto">
                    <span class="nav-link">
                        <i class="fas fa-tachometer-alt"></i> Global Dashboard
                    </span>
                </div>
                
                <div class="navbar-nav">
                    <span class="navbar-text text-dark fw-bold me-3">
                        <i class="fas fa-flag text-success"></i> Morocco 🇲🇦
                    </span>
                    <a href="https://www.linkedin.com/in/baroudi-mustapha-2a257a289/" 
                       target="_blank" class="btn btn-outline-primary btn-sm">
                        <i class="fab fa-linkedin"></i> Developer
                    </a>
                </div>
            </div>
        </nav>

        <!-- Main Content -->
        <div class="container-fluid py-4">
            <div class="row mb-4">
                <div class="col-12 text-center">
                    <h1 class="fw-bold mb-3">
                        <i class="fas fa-globe text-primary"></i> SIMS - Live Worldwide!
                    </h1>
                    <p class="text-muted fs-5">Smart Inventory Management System</p>
                    <p class="text-success fw-bold">✅ Accessible from anywhere in the world!</p>
                </div>
            </div>

            <!-- Metrics Cards -->
            <div class="row mb-5">
                <div class="col-md-3 mb-4">
                    <div class="card metric-card primary text-white">
                        <div class="card-body text-center">
                            <h2 class="fw-bold mb-1">5</h2>
                            <p class="mb-0 opacity-90">Total Products</p>
                            <small class="opacity-75">Active inventory</small>
                        </div>
                    </div>
                </div>
                <div class="col-md-3 mb-4">
                    <div class="card metric-card success text-white">
                        <div class="card-body text-center">
                            <h2 class="fw-bold mb-1">18,840 MAD</h2>
                            <p class="mb-0 opacity-90">Inventory Value</p>
                            <small class="opacity-75">Total worth</small>
                        </div>
                    </div>
                </div>
                <div class="col-md-3 mb-4">
                    <div class="card metric-card info text-white">
                        <div class="card-body text-center">
                            <h2 class="fw-bold mb-1">23</h2>
                            <p class="mb-0 opacity-90">Sales (7 days)</p>
                            <small class="opacity-75">Recent activity</small>
                        </div>
                    </div>
                </div>
                <div class="col-md-3 mb-4">
                    <div class="card metric-card warning text-white">
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
                                <i class="fas fa-rocket text-warning"></i> Professional Features
                            </h5>
                        </div>
                        <div class="card-body">
                            <div class="row">
                                <div class="col-md-3 mb-3">
                                    <div class="text-center p-3 rounded" style="background: rgba(102, 126, 234, 0.1);">
                                        <i class="fas fa-chart-line text-primary fs-1 mb-3"></i>
                                        <h6 class="fw-bold">Real-time Analytics</h6>
                                        <p class="text-muted small">Live business metrics</p>
                                    </div>
                                </div>
                                <div class="col-md-3 mb-3">
                                    <div class="text-center p-3 rounded" style="background: rgba(40, 167, 69, 0.1);">
                                        <i class="fas fa-shopping-cart text-success fs-1 mb-3"></i>
                                        <h6 class="fw-bold">Point of Sale</h6>
                                        <p class="text-muted small">Complete sales system</p>
                                    </div>
                                </div>
                                <div class="col-md-3 mb-3">
                                    <div class="text-center p-3 rounded" style="background: rgba(255, 193, 7, 0.1);">
                                        <i class="fas fa-boxes text-warning fs-1 mb-3"></i>
                                        <h6 class="fw-bold">Inventory Control</h6>
                                        <p class="text-muted small">Smart stock management</p>
                                    </div>
                                </div>
                                <div class="col-md-3 mb-3">
                                    <div class="text-center p-3 rounded" style="background: rgba(220, 53, 69, 0.1);">
                                        <i class="fas fa-mobile-alt text-danger fs-1 mb-3"></i>
                                        <h6 class="fw-bold">Mobile Ready</h6>
                                        <p class="text-muted small">Works on all devices</p>
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
                                Professional inventory management system now live and accessible globally.
                                Perfect for LinkedIn portfolio and professional showcasing!
                            </p>
                            <div class="row justify-content-center">
                                <div class="col-md-8">
                                    <div class="row">
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
                                                <strong>+212 697 362 759</strong>
                                            </a>
                                        </div>
                                        <div class="col-md-4 mb-3">
                                            <a href="mailto:mustaphabaroudi833@gmail.com" class="btn btn-light w-100">
                                                <i class="fas fa-envelope"></i><br>
                                                <strong>Email Me</strong>
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

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
'''

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
