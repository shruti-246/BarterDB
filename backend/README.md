# 🛍️ BarterDB Backend (Django + DRF)

This is the backend of the **BarterDB** project — a full-stack bartering app built using **Django** and **Django REST Framework**. It powers a native Android frontend and supports user authentication, product listings, trades, and QR code-based verification.

---

## Features

### User Management
- Custom user model with roles (`buyer`, `seller`)
- Register: `/api/register/` (POST)
- Login: `/api/login/` (POST, returns token)
- Token-based authentication using `rest_framework.authtoken`

### Product Management
- List all products: `GET /api/products/`
- Add new product: `POST /api/products/`
- Edit/Delete your own product: `PUT/DELETE /api/products/<id>/`
- View your products: `GET /api/my-products/`

### Barter Trade System
- Create a trade offer: `POST /api/trades/`
- View your sent trades: `GET /api/my-trades/sent/`
- View your received trades: `GET /api/my-trades/received/`
- Accept/decline a trade: `POST /api/trades/<id>/update-status/`
- View trade history: `GET /api/my-trades/history/`

### QR Code Integration
- On trade acceptance, a QR code is auto-generated.
- QR code model is linked to accepted trades (`QRCode` model).
- QR image is stored in the `media/qrcodes/` folder.

---

## Tech Stack

- Python 3.12+
- Django 5.2
- Django REST Framework
- SQLite (development) / MySQL/MariaDB (optional)
- qrcode (Python lib)

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/shruti-246/BarterDB.git
cd BarterDB/backend

#create virtual environment
python -m venv venv
venv\Scripts\activate

#Install Requirements
pip install -r requirements.txt

#Or manually
pip install django djangorestframework djangorestframework-simplejwt qrcode pillow

#Run Migrations
python manage.py makemigrations
python manage.py migrate

#Create Superuser
python manage.py createsuperuser

#Run Server
python manage.py runserver

