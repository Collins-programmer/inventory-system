# Inventory Management API

## Overview

This project is a Flask-based Inventory Management API that provides RESTful endpoints for managing inventory items. It integrates with the OpenFoodFacts API to automatically retrieve product information using a barcode, reducing manual data entry. A command-line interface (CLI) is included for interacting with the API, and automated tests are provided using Pytest.

## Features

- View all inventory items
- Retrieve a single inventory item
- Add new products using barcode lookup
- Update product price and stock quantity
- Delete inventory items
- OpenFoodFacts API integration for product metadata
- Command-line interface for interacting with the API
- Automated unit tests using Pytest

## Prerequisites

Before getting started, ensure the following are installed:

- Python 3.10 or later
- Git
- Pipenv

Install Pipenv if it is not already available use:
```
pip install pipenv
```

## Clone the Repository

Clone the repository and navigate into the project directory.
```
git clone <your-ssh-link >
cd <repository-name>
```

## Install Dependencies

Create a virtual environment and install all project dependencies using Pipenv.

```
pipenv install
```
Activate the virtual environment.
```
pipenv shell
```
Since the project includes development dependencies, install them as well.
```
pipenv install --dev
```

## Running the Application

Start the Flask application.
```
python app.py
```

The API will be available at:
```
http://127.0.0.1:5000
```

## Running the Command-Line Interface

Once the API server is running, start the CLI in a separate terminal.
```
python cli.py
```
The CLI provides options to:

- View all inventory items
- View a specific inventory item
- Add a new product
- Update price and stock
- Delete a product
- Perform a barcode lookup using OpenFoodFacts

## API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | `/inventory` | Retrieve all inventory items |
| GET | `/inventory/<id>` | Retrieve a single inventory item |
| POST | `/inventory` | Add a new inventory item |
| PATCH | `/inventory/<id>` | Update an existing inventory item |
| DELETE | `/inventory/<id>` | Delete an inventory item |

## Running Tests

Execute the test suite using Pytest.
```
pytest
```
To display more detailed test output:
```
pytest -v
```
## External API

This project uses the OpenFoodFacts API to retrieve product information based on barcode values.

When a valid barcode is provided, the application attempts to fetch:

- Product name
- Brand
- Ingredients

If the product cannot be found, default values are used instead.

## Technologies Used

- Python
- Flask
- Requests
- Pipenv
- Pytest

## License

This project is intended for educational purposes. Modify and distribute it as needed.