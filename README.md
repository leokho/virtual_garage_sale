# Virtual Garage Sale

This is a simple Flask-based web application that allows you to create a virtual garage sale. You can upload a CSV file with item details, and the application will display them on a public HTML page. Each item can have a title, description, price, status, and image URL.

## Features

- Upload a CSV file to list items for sale.
- Display items with title, description, price, status, and image.
- Color-coded status labels for RESERVED (orange) and SOLD (red).
- Responsive and mobile-friendly design.

## Requirements

- Python 3.6+
- Flask

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/virtual-garage-sale.git
    cd virtual-garage-sale
    ```

2. Install the required packages:
    ```bash
    pip install flask
    ```

3. Create the necessary directories:
    ```bash
    mkdir -p uploads static/images
    ```

## Usage

1. Run the Flask application:
    ```bash
    python app.py
    ```

2. Open your browser and go to `http://127.0.0.1:5000/upload` to upload your CSV file.

3. After uploading the CSV, visit `http://127.0.0.1:5000/` to view the listed items.

## CSV Format

The CSV file should have the following columns:
- `Title`: The title of the item.
- `Description`: A description of the item.
- `Price`: The price of the item.
- `Status`: The status of the item (e.g., AVAILABLE, RESERVED, SOLD).
- `Image URL`: The URL of the item's image.

### Example CSV

```csv
Title,Description,Price,Status,Image URL
Bike,Mountain bike in good condition,150,Available,https://example.com/images/bike.jpg
Laptop,15 inch laptop with 8GB RAM,300,RESERVED,https://example.com/images/laptop.jpg
Table,Wooden dining table,100,SOLD,https://example.com/images/table.jpg
