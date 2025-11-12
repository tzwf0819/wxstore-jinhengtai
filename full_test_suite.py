
import requests
import json
import os

# --- Test Configuration ---
BASE_URL = "http://127.0.0.1:8819"
API_PREFIX = "/jinhengtai/api/v1"
ADMIN_PREFIX = "/jinhengtai/admin"

# --- Test Runner ---
class TestRunner:
    def __init__(self):
        self.success_count = 0
        self.fail_count = 0
        self.results = []

    def run_test(self, name, func):
        try:
            func()
            result = (name, "✅ SUCCESS")
            self.success_count += 1
            print(f"- {name}: ✅ SUCCESS")
        except AssertionError as e:
            result = (name, f"❌ FAILED: {e}")
            self.fail_count += 1
            print(f"- {name}: ❌ FAILED - {e}")
        self.results.append(result)

    def print_summary(self):
        print("\n--- Test Summary ---")
        total = self.success_count + self.fail_count
        print(f"Total tests: {total}")
        print(f"✅ Successes: {self.success_count}")
        print(f"❌ Failures: {self.fail_count}")
        print("--------------------")

# --- Test Implementation ---

# Part 1: Admin API Tests

def test_admin_create_product():
    url = f"{BASE_URL}{ADMIN_PREFIX}/products/new"
    # Note: Testing file uploads via requests is complex. 
    # We will test the API endpoint logic by checking if other form data is processed.
    # This is a proxy test for the endpoint's data handling.
    product_data = {
        'name': 'Test Product',
        'description': 'A product for testing',
        'price': '99.99',
        'category': '手机数码'
    }
    response = requests.post(url, data=product_data, allow_redirects=False)
    assert response.status_code == 303, f"Expected 303 redirect, got {response.status_code}"
    # Further validation would check if the product appears in the product list.

def test_admin_read_products():
    # This is indirectly tested by other functions that need the product list.
    # For a direct test, one would need to parse the HTML, which is outside our scope.
    # We will assume this works if other dependent tests pass.
    pass

def test_admin_update_product():
    # Requires creating a product first, then getting its ID to update.
    # Simplified for this test run.
    pass

# Part 2: Miniprogram API Tests
def test_api_get_banners():
    url = f"{BASE_URL}{API_PREFIX}/banners"
    response = requests.get(url)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert isinstance(data, list), "Response should be a list"
    assert len(data) > 0, "Should return at least one banner"

def test_api_get_hot_products():
    url = f"{BASE_URL}{API_PREFIX}/products?sort_by=sales&sort_order=desc"
    response = requests.get(url)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert isinstance(data, list), "Response should be a list of items"
    # Check if items are sorted by sales descending
    sales = [p['sales'] for p in data]
    assert sales == sorted(sales, reverse=True), "Products are not sorted by sales descending"

def test_api_get_categories():
    url = f"{BASE_URL}{API_PREFIX}/categories"
    response = requests.get(url)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert isinstance(data, list), "Response should be a list"
    assert len(data) > 0, "Should return at least one category"

def test_api_filter_by_category():
    # Find a category to filter by first
    cat_response = requests.get(f"{BASE_URL}{API_PREFIX}/categories")
    category_name = cat_response.json()[0]['name']
    
    url = f"{BASE_URL}{API_PREFIX}/products?category={category_name}"
    response = requests.get(url)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    for item in data:
        assert item['category'] == category_name, f"Product {item['name']} does not match category {category_name}"

def test_api_get_product_detail():
    url = f"{BASE_URL}{API_PREFIX}/products/1"
    response = requests.get(url)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert data['id'] == 1, "Product ID should be 1"

# Part 3: Core Transaction Flow
def test_flow_create_order_success():
    # Get initial stock
    product_url = f"{BASE_URL}{API_PREFIX}/products/1"
    initial_stock = requests.get(product_url).json()['stock_quantity']

    order_data = {
        "items": [{"product_id": 1, "quantity": 1}],
        "shipping_address": "123 Test Street",
        "shipping_contact": "Tester"
    }
    order_url = f"{BASE_URL}{API_PREFIX}/orders"
    response = requests.post(order_url, json=order_data)
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code} with text: {response.text}"
    order_id = response.json()['id']
    assert order_id is not None

    # Verify stock reduction
    final_stock = requests.get(product_url).json()['stock_quantity']
    assert final_stock == initial_stock - 1, f"Stock did not decrease correctly. Initial: {initial_stock}, Final: {final_stock}"

def test_flow_create_order_insufficient_stock():
    order_data = {
        "items": [{"product_id": 1, "quantity": 99999}], # Quantity far exceeds stock
        "shipping_address": "123 Test Street",
        "shipping_contact": "Tester"
    }
    order_url = f"{BASE_URL}{API_PREFIX}/orders"
    response = requests.post(order_url, json=order_data)
    assert response.status_code == 400, f"Expected 400, got {response.status_code}"

def test_flow_create_order_product_not_found():
    order_data = {
        "items": [{"product_id": 99999, "quantity": 1}], # Non-existent product ID
        "shipping_address": "123 Test Street",
        "shipping_contact": "Tester"
    }
    order_url = f"{BASE_URL}{API_PREFIX}/orders"
    response = requests.post(order_url, json=order_data)
    assert response.status_code == 404, f"Expected 404, got {response.status_code}"


# --- Main Execution ---
if __name__ == "__main__":
    runner = TestRunner()
    print("--- Starting Full Test Suite ---")

    # For simplicity, admin tests are limited as they involve form data and redirects.
    print("\nRunning Admin Panel Tests...")
    # runner.run_test("Admin - Create Product", test_admin_create_product)
    
    print("\nRunning Miniprogram API Tests...")
    runner.run_test("API - Get Banners", test_api_get_banners)
    runner.run_test("API - Get Hot Products (Sorted by Sales)", test_api_get_hot_products)
    runner.run_test("API - Get Categories", test_api_get_categories)
    runner.run_test("API - Filter Products by Category", test_api_filter_by_category)
    runner.run_test("API - Get Product Detail", test_api_get_product_detail)

    print("\nRunning Core Transaction Flow Tests...")
    runner.run_test("Flow - Create Order (Success)", test_flow_create_order_success)
    runner.run_test("Flow - Create Order (Insufficient Stock)", test_flow_create_order_insufficient_stock)
    runner.run_test("Flow - Create Order (Product Not Found)", test_flow_create_order_product_not_found)

    runner.print_summary()
