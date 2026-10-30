# Ecommerce Shipping Box Recommendation System

## Project Overview

The Ecommerce Shipping Box Recommendation System is a Django-based web application designed to manage customer purchases and recommend suitable shipping boxes for completed orders.

Customers can register, log in, view products, purchase products, and check their order summaries. Packaging staff can log in separately, view completed customer orders, and calculate suitable shipping boxes based on product dimensions and weight.

## Features

### Customer Module
- Customer registration and login.
- View available products.
- Purchase products.
- Continue shopping or finish a purchase.
- View completed order summaries.

### Packaging Staff Module
- Separate staff account creation.
- Separate packaging staff login.
- Access the warehouse dashboard.
- View completed customer orders.
- Calculate suitable shipping boxes.
- View packing details and total box cost.

## Technologies Used

- Python
- Django
- HTML
- CSS
- SQLite Database

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/santhanamari2006/shipping_box_recommender.git
```

### 2. Navigate to the project directory

```bash
cd shipping_box_recommender
```

### 3. Activate the virtual environment

Windows:

```bash
.venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install django pillow
```

### 5. Apply database migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create a manager account

```bash
python manage.py createsuperuser
```

### 7. Start the development server

```bash
python manage.py runserver
```

### 8. Open the application

```text
http://127.0.0.1:8000/
```

## Application Workflow

1. Customers register and log in.
2. Customers browse available products.
3. Customers purchase products.
4. Customers complete their orders.
5. Packaging staff log in separately.
6. Staff view completed orders in the warehouse dashboard.
7. Staff calculate suitable shipping boxes for each order.

## Notes

- Customer and packaging staff accounts have separate login processes.
- The application uses SQLite as its database.
- The shipping box recommendation depends on product dimensions, weight, and available box specifications.