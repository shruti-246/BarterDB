# BarterDB - MVP (Minimum Viable Product)

**BarterDB** is a database-driven barter application that enables users to list, browse, and request item trades. This repository contains the **MVP version** of the project, developed as part of a software engineering coursework project.

The MVP focuses on core features such as **user authentication** and **item listing**, with future plans to support barter requests, messaging, and QR code-based transactions.

---

## 📌 Key Features (MVP)

- 🔐 **User Authentication** (Sign Up, Login, Logout)
- 👤 **User Profiles**
- 📦 **Item Listing** (Add/View Items)

---

## 🧰 Technologies Used

- **Backend:** Django, Django REST Framework  
- **Database:** SQLite (switched from MySQL due to compatibility issues with MariaDB)  
- **Frontend (MVP):** HTML, CSS  
- **Future Frontend:** Kotlin (Jetpack Compose) for mobile app interface

---

## 📁 Project Structure


---

## 🚀 Getting Started (Local Setup)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/barterdb_mvp.git
   cd barterdb_mvp

2. **Set up the virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt

4. **Apply Migrations:**
   ```bash
   python manage.py migrate

5. **Run the development server:**
   ```bash
  python manage.py runserver
6. **Access the app:**
  Open your browser and go to http://127.0.0.1:8000/
