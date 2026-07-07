from flask import Flask, jsonify, request
import requests

app = Flask(__name__)


inventory_db = [
    {
        "id": "1",
        "barcode": "0041196910759",
        "product_name": "Organic Almond Milk",
        "brands": "Silk",
        "ingredients_text": "Filtered water, almonds, cane sugar, sea salt",
        "price": 3.99,
        "quantity": 45
    },
    {
        "id": "2",
        "barcode": "5449000000439",
        "product_name": "Coca-Cola Classic",
        "brands": "Coca-Cola",
        "ingredients_text": "Carbonated water, sugar, color (Caramel E150d), phosphoric acid",
        "price": 1.49,
        "quantity": 120
    }
]

# Helper function to query OpenFoodFacts API
def fetch_external_product(barcode):
    url = f"https://world.openfoodfacts.org/api/v2/product/{barcode}.json"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == 1:
                product_data = data.get("product", {})
                return {
                    "product_name": product_data.get("product_name", "Unknown Product"),
                    "brands": product_data.get("brands", "Unknown Brand"),
                    "ingredients_text": product_data.get("ingredients_text", "No ingredients provided.")
                }
    except requests.RequestException:
        pass
    return None

@app.route('/inventory', methods=['GET'])
def get_all_items():
    return jsonify(inventory_db), 200

@app.route('/inventory/<string:item_id>', methods=['GET'])
def get_item(item_id):
    item = next((i for i in inventory_db if i["id"] == item_id), None)
    if item:
        return jsonify(item), 200
    return jsonify({"error": "Item not found"}), 404

@app.route('/inventory', methods=['POST'])
def add_item():
    data = request.get_json() or {}
    barcode = data.get("barcode")
    price = data.get("price")
    quantity = data.get("quantity")

    if not all([barcode, price, quantity]):
        return jsonify({"error": "Missing required fields: barcode, price, quantity"}), 400

    # Prevent duplicate records for simplicity
    if any(i["barcode"] == str(barcode) for i in inventory_db):
        return jsonify({"error": "Product with this barcode already exists in inventory"}), 400

    # Fetch enrichment data from OpenFoodFacts
    external_data = fetch_external_product(barcode)
    if not external_data:
        # Fallback details if external API fails or product isn't found
        external_data = {
            "product_name": data.get("product_name", "Generic Product"),
            "brands": data.get("brands", "Generic Brand"),
            "ingredients_text": "N/A"
        }

    new_id = str(max([int(i["id"]) for i in inventory_db]) + 1) if inventory_db else "1"
    
    new_item = {
        "id": new_id,
        "barcode": str(barcode),
        "product_name": external_data["product_name"],
        "brands": external_data["brands"],
        "ingredients_text": external_data["ingredients_text"],
        "price": float(price),
        "quantity": int(quantity)
    }
    
    inventory_db.append(new_item)
    return jsonify(new_item), 201

@app.route('/inventory/<string:item_id>', methods=['PATCH'])
def update_item(item_id):
    item = next((i for i in inventory_db if i["id"] == item_id), None)
    if not item:
        return jsonify({"error": "Item not found"}), 404

    data = request.get_json() or {}
    if "price" in data:
        item["price"] = float(data["price"])
    if "quantity" in data:
        item["quantity"] = int(data["quantity"])

    return jsonify(item), 200

@app.route('/inventory/<string:item_id>', methods=['DELETE'])
def delete_item(item_id):
    global inventory_db
    item = next((i for i in inventory_db if i["id"] == item_id), None)
    if not item:
        return jsonify({"error": "Item not found"}), 404

    inventory_db = [i for i in inventory_db if i["id"] != item_id]
    return jsonify({"message": f"Item {item_id} successfully deleted"}), 200

if __name__ == '__main__':
   
    app.run(port=5000, debug=True)