
import requests
import json
import os

# --- Test Configuration ---
BASE_URL = "http://127.0.0.1:8819"
# The admin routes are part of the root path in the web router
ADMIN_URL_PREFIX = f"{BASE_URL}/admin"
PROXIES = {"http": None, "https": None}

# --- Test Runner ---
class TestRunner:
    def __init__(self):
        self.success_count = 0
        self.fail_count = 0

    def run_test(self, name, func):
        try:
            print(f"- Running: {name}...")
            func()
            self.success_count += 1
            print(f"  -> ✅ SUCCESS")
        except AssertionError as e:
            self.fail_count += 1
            print(f"  -> ❌ FAILED: {e}")

    def print_summary(self):
        print("\n--- Admin Test Summary ---")
        total = self.success_count + self.fail_count
        print(f"Total tests: {total}")
        print(f"✅ Successes: {self.success_count}")
        print(f"❌ Failures: {self.fail_count}")
        print("------------------------")

# --- Test Implementation ---

def test_category_crud():
    # 1. Create a category
    create_data = {"name": "Test Category"}
    create_resp = requests.post(f"{ADMIN_URL_PREFIX}/categories/new", data=create_data, allow_redirects=False, proxies=PROXIES)
    assert create_resp.status_code == 303, f"Category creation should redirect (303), got {create_resp.status_code}"

    # 2. Find the created category for editing/deleting (this is complex without reading HTML)
    # For this test, we assume creation works and move on. A full test would need to parse the response.


def test_product_create_and_update():
    # 1. Create a product
    product_data = {
        'name': 'Laptop 123',
        'description': 'A new laptop model',
        'price': '1299.99',
        'category': '手机数码'
    }
    create_resp = requests.post(f"{ADMIN_URL_PREFIX}/products/new", data=product_data, allow_redirects=False, proxies=PROXIES)
    assert create_resp.status_code == 303, f"Product creation should redirect (303), got {create_resp.status_code}"

    # 2. Update a product (using product_id=1 from initial_data)
    update_data = {
        'name': 'Updated Smartphone Pro',
        'description': 'Updated description',
        'price': '5199.00',
        'category': '手机数码'
    }
    update_resp = requests.post(f"{ADMIN_URL_PREFIX}/products/edit/1", data=update_data, allow_redirects=False, proxies=PROXIES)
    assert update_resp.status_code == 303, f"Product update should redirect (303), got {update_resp.status_code}"

def test_banner_crud():
    # Test banner creation (without file upload)
    banner_data = {
        'link_url': '/products/1',
        'sort_order': '10',
        'is_active': 'true'
    }
    # This request will fail because the 'image' file is required. We expect a 422 or 500 error.
    # This tests the server's handling of missing required files.
    create_resp = requests.post(f"{ADMIN_URL_PREFIX}/banners/new", data=banner_data, allow_redirects=False, proxies=PROXIES)
    assert create_resp.status_code != 200, f"Banner creation without image should fail, but got {create_resp.status_code}"

    # Test banner deletion (using banner_id=1 from initial_data)
    delete_resp = requests.post(f"{ADMIN_URL_PREFIX}/banners/delete/1", allow_redirects=False, proxies=PROXIES)
    assert delete_resp.status_code == 303, f"Banner deletion should redirect (303), got {delete_resp.status_code}"


# --- Main Execution ---
if __name__ == "__main__":
    runner = TestRunner()
    print("--- Starting Admin Panel WRITE Test Suite ---")
    
    # Note: These tests are simplified. A full suite would require a way to get the ID 
    # of a newly created item to perform update/delete on it.

    runner.run_test("Category - Create", test_category_crud)
    runner.run_test("Product - Create & Update", test_product_create_and_update)
    runner.run_test("Banner - Create (Negative) & Delete", test_banner_crud)
    
    runner.print_summary()
