import requests
import json

# The URL for the create_order endpoint
url = "http://127.0.0.1:8819/jinhengtai/api/v1/orders/"

# --- Test Data ---
# This simulates an order for two different products.
# Ensure that product_id 1 and 2 exist in your database and have enough stock.
order_data = {
    "items": [
        {
            "product_id": 1,  # Assuming a product with ID 1 exists
            "quantity": 2
        },
        {
            "product_id": 2,  # Assuming a product with ID 2 exists
            "quantity": 1
        }
    ],
    "shipping_address": "123 Test Street, Suite 456, Testville, TS 78910",
    "shipping_contact": "John Doe - 555-123-4567"
}

# --- Sending the Request ---
headers = {
    'Content-Type': 'application/json'
}

print(f"Sending POST request to {url} with data:")
print(json.dumps(order_data, indent=2))

try:
    response = requests.post(url, headers=headers, data=json.dumps(order_data))

    # --- Analyzing the Response ---
    print(f"\n--- Server Response ---")
    print(f"Status Code: {response.status_code}")

    if response.status_code == 200:
        print("\nSUCCESS: The order was created successfully!")
        print("Response JSON:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    elif response.status_code == 500:
        print("\nERROR: The server returned a 500 Internal Server Error.")
        print("This indicates a bug in the backend code.")
        print("Raw Response Text:")
        print(response.text)
    elif response.status_code == 404:
        print("\nERROR: The server returned a 404 Not Found.")
        print("Please check if the URL is correct and the server is running.")
    else:
        print(f"\nUNEXPECTED RESPONSE: Received status code {response.status_code}")
        print("Raw Response Text:")
        print(response.text)

except requests.exceptions.ConnectionError as e:
    print(f"\nCONNECTION ERROR: Could not connect to the server at {url}.")
    print("Please ensure that the backend server is running and accessible.")

