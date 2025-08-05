#!/usr/bin/env python3
"""
Simple test script to verify the SIMS application works
"""

import os
import sys
import tempfile
from app import create_app, db

def test_app_creation():
    """Test that the app can be created successfully"""
    print("Testing app creation...")
    
    # Create app with testing configuration
    app = create_app('testing')
    
    with app.app_context():
        # Test database creation
        print("Creating database tables...")
        db.create_all()
        
        # Test that tables were created
        from app.models import Product, Category, Supplier, Sale, SaleItem, InventoryTransaction
        
        # Create test data
        print("Creating test data...")
        
        # Create category
        category = Category(name="Test Category", description="Test category for testing")
        category.save()
        
        # Create supplier
        supplier = Supplier(
            name="Test Supplier",
            contact_person="John Doe",
            email="john@testsupplier.com",
            phone="+212-123-456789"
        )
        supplier.save()
        
        # Create product
        product = Product(
            name="Test Product",
            sku="TEST-001",
            category_id=category.id,
            supplier_id=supplier.id,
            unit_price=100.0,
            cost_price=60.0,
            current_stock=50,
            reorder_level=10,
            safety_stock=5
        )
        product.save()
        
        print(f"Created product: {product.name} (ID: {product.id})")
        print(f"Product stock status: {product.stock_status}")
        print(f"Product inventory value: {product.inventory_value} MAD")
        print(f"Product profit margin: {product.profit_margin:.2f}%")
        
        # Test EOQ calculation
        eoq = product.calculate_eoq()
        print(f"Economic Order Quantity: {eoq}")
        
        # Test stock update
        print("Testing stock update...")
        new_stock = product.update_stock(-5, 'SALE', 'Test sale')
        print(f"Stock after sale: {new_stock}")
        
        # Test inventory transaction creation
        transactions = product.inventory_transactions.all()
        print(f"Number of transactions: {len(transactions)}")
        
        # Test ABC classification
        product.abc_classification = 'A'
        db.session.commit()
        print(f"ABC Classification: {product.abc_classification}")
        
        print("✅ All tests passed!")
        return True

def test_routes():
    """Test that main routes work"""
    print("\nTesting routes...")
    
    app = create_app('testing')
    
    with app.test_client() as client:
        # Test main dashboard
        response = client.get('/')
        print(f"Dashboard route status: {response.status_code}")
        assert response.status_code == 200
        
        # Test API endpoints
        response = client.get('/api/dashboard')
        print(f"API dashboard status: {response.status_code}")
        assert response.status_code == 200
        
        # Test health check
        response = client.get('/health')
        print(f"Health check status: {response.status_code}")
        assert response.status_code == 200
        
        print("✅ Route tests passed!")
        return True

def main():
    """Run all tests"""
    print("🚀 Starting SIMS Application Tests")
    print("=" * 50)
    
    try:
        # Test app creation and models
        test_app_creation()
        
        # Test routes
        test_routes()
        
        print("\n" + "=" * 50)
        print("🎉 All tests completed successfully!")
        print("The SIMS application is ready to run!")
        print("\nTo start the application:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Initialize database: python run.py init-db")
        print("3. Run the app: python run.py")
        print("4. Open browser to: http://localhost:5000")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
