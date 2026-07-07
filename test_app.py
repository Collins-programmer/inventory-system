import pytest
from unittest.mock import patch
from app import app, inventory_db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        global inventory_db
        inventory_db.clear()
        inventory_db.extend([
            {"id": "1", "barcode": "1111", "product_name": "Test Item 1", "brands": "Brand A", "ingredients_text": "Water", "price": 1.0, "quantity": 10},
            {"id": "2", "barcode": "2222", "product_name": "Test Item 2", "brands": "Brand B", "ingredients_text": "Sugar", "price": 2.0, "quantity": 20}
        ])
        yield client

def test_get_all_items(client):
    response = client.get('/inventory')
    assert response.status_code == 200
    assert len(response.get_json()) == 2

def test_get_single_item_success(client):
    response = client.get('/inventory/1')
    assert response.status_code == 200
    assert response.get_json()["product_name"] == "Test Item 1"

def test_get_single_item_not_found(client):
    response = client.get('/inventory/999')
    assert response.status_code == 404

# Mocking external network requests when hitting the POST endpoint
@patch('app.requests.get')
def test_add_item_with_external_api(mock_get, client):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "status": 1,
        "product": {
            "product_name": "Mocked Coconut Water",
            "brands": "Vita-Mock",
            "ingredients_text": "Organic Coconuts"
        }
    }

    payload = {"barcode": "3333", "price": 4.50, "quantity": 30}
    response = client.post('/inventory', json=payload)
    
    assert response.status_code == 201
    json_data = response.get_json()
    assert json_data["id"] == "3"
    assert json_data["product_name"] == "Mocked Coconut Water"
    assert json_data["brands"] == "Vita-Mock"

def test_patch_item_modifications(client):
    update_payload = {"price": 1.50, "quantity": 15}
    response = client.patch('/inventory/1', json=update_payload)
    assert response.status_code == 200
    
    json_data = response.get_json()
    assert json_data["price"] == 1.50
    assert json_data["quantity"] == 15

def test_delete_item_execution(client):
    response = client.delete('/inventory/2')
    assert response.status_code == 200
    
    
    check_response = client.get('/inventory/2')
    assert check_response.status_code == 404