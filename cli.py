import sys
import requests

BASE_URL = "http://127.0.0.1:5000/inventory"

def print_menu():
    print("\n=== INVENTORY MANAGEMENT PORTAL ===")
    print("1. View All Inventory")
    print("2. View Single Item Details")
    print("3. Add New Item (with OpenFoodFacts Auto-Lookup)")
    print("4. Update Item Price/Stock")
    print("5. Delete Product")
    print("6. Lookup Barcode Raw Info via API")
    print("7. Exit")
    print("===================================\n")

def view_all():
    try:
        res = requests.get(BASE_URL)
        if res.status_code == 200:
            items = res.json()
            print(f"\n{'ID':<5} | {'Name':<25} | {'Brand':<15} | {'Price':<8} | {'Stock':<6}")
            print("-" * 65)
            for item in items:
                print(f"{item['id']:<5} | {item['product_name'][:24]:<25} | {item['brands'][:14]:<15} | ${item['price']:<7.2f} | {item['quantity']:<6}")
        else:
            print("Failed to fetch data.")
    except requests.ConnectionError:
        print("Error: Ensure your Flask API is running on port 5000.")

def view_single():
    item_id = input("Enter Item ID to view: ").strip()
    try:
        res = requests.get(f"{BASE_URL}/{item_id}")
        if res.status_code == 200:
            item = res.json()
            print(f"\n--- Product Details [{item['id']}] ---")
            print(f"Barcode:     {item['barcode']}")
            print(f"Name:        {item['product_name']}")
            print(f"Brand:       {item['brands']}")
            print(f"Price:       ${item['price']:.2f}")
            print(f"Stock Level: {item['quantity']}")
            print(f"Ingredients: {item['ingredients_text']}")
        else:
            print(f"Error: {res.json().get('error', 'Item not found.')}")
    except requests.ConnectionError:
        print("Error: Could not connect to API server.")

def add_item():
    barcode = input("Enter Barcode: ").strip()
    try:
        price = float(input("Enter Base Retail Price ($): "))
        quantity = int(input("Enter Starting Stock Quantity: "))
    except ValueError:
        print("Invalid number input. Aborting addition.")
        return

    payload = {"barcode": barcode, "price": price, "quantity": quantity}
    try:
        res = requests.post(BASE_URL, json=payload)
        if res.status_code == 201:
            item = res.json()
            print(f"\n[SUCCESS] Added: {item['product_name']} ({item['brands']}) mapped to internal ID {item['id']}.")
        else:
            print(f"Error: {res.json().get('error', 'Could not save item.')}")
    except requests.ConnectionError:
        print("Error: Could not reach the API backend server.")

def update_item():
    item_id = input("Enter Item ID to modify: ").strip()
    print("Leave field blank if you do not want to change it.")
    price_input = input("Enter New Price (or Enter to skip): ").strip()
    qty_input = input("Enter New Stock Level (or Enter to skip): ").strip()

    payload = {}
    if price_input:
        payload["price"] = float(price_input)
    if qty_input:
        payload["quantity"] = int(qty_input)

    if not payload:
        print("No changes specified.")
        return

    try:
        res = requests.patch(f"{BASE_URL}/{item_id}", json=payload)
        if res.status_code == 200:
            print("[SUCCESS] Item updated successfully.")
        else:
            print(f"Error: {res.json().get('error', 'Update failed.')}")
    except requests.ConnectionError:
         print("Error: Connectivity failed.")

def delete_item():
    item_id = input("Enter Item ID to DELETE: ").strip()
    confirm = input(f"Are you absolutely sure you want to delete item {item_id}? (y/N): ").strip().lower()
    if confirm != 'y':
        print("Deletion canceled.")
        return

    try:
        res = requests.delete(f"{BASE_URL}/{item_id}")
        if res.status_code == 200:
            print(f"[SUCCESS] {res.json().get('message')}")
        else:
            print(f"Error: {res.json().get('error')}")
    except requests.ConnectionError:
        print("Error: Communication break with API backend.")

def external_lookup():
    barcode = input("Enter target barcode to scan on OpenFoodFacts: ").strip()
    url = f"https://world.openfoodfacts.org/api/v2/product/{barcode}.json"
    print("Pinging OpenFoodFacts live global database...")
    try:
        res = requests.get(url, timeout=5)
        if res.status_code == 200 and res.json().get("status") == 1:
            p = res.json()["product"]
            print(f"\nLive Metadata Found:")
            print(f"  Title: {p.get('product_name', 'N/A')}")
            print(f"  Brand: {p.get('brands', 'N/A')}")
        else:
            print("Product not resolved in the OpenFoodFacts global database.")
    except Exception as e:
        print(f"Request failed: {e}")

def main():
    while True:
        print_menu()
        choice = input("Select an option (1-7): ").strip()
        if choice == "1":
            view_all()
        elif choice == "2":
            view_single()
        elif choice == "3":
            add_item()
        elif choice == "4":
            update_item()
        elif choice == "5":
            delete_item()
        elif choice == "6":
            external_lookup()
        elif choice == "7":
            print("Exiting portal. Goodbye!")
            sys.exit(0)
        else:
            print("Invalid input choice. Try again.")

if __name__ == "__main__":
    main()