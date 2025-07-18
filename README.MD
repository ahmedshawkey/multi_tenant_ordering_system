# 🧠 Multi-Tenant Ordering System (Django)

A robust backend application for managing products and orders in a multi-tenant architecture.  
Built with Django, MySQL, and role-based authentication — featuring both REST APIs and an HTML admin interface.

---

## 🚀 Features

- 🔐 JWT-based authentication with custom `admin`, `operator`, and `viewer` roles
- 📝 Product creation & listing with real-time stock management
- 📦 Order creation with auto-fill logic, validation, and shipping simulation
- 🧑‍💼 Admin panel with CSV export and bulk actions
- 🖥️ Simple HTML interface for non-technical users
- 🧠 Role-aware access control:
  - Viewers cannot place orders
  - Operators can only edit orders created today
  - Email confirmation logging via file write on order shipping

---

## 🛠️ Tech Stack

| Tool | Usage |
|------|-------|
| Django | Core backend framework |
| Django REST Framework | APIs for products and orders |
| MySQL | Tenant-aware data storage |
| JWT | Secure authentication |
| HTML Templates | Admin interface |
| Pipenv | Dependency management |

---

## ⚙️ Setup Instructions

```bash
git clone https://github.com/ahmedshawkey/multi_tenant_ordering_system.git
cd multi_tenant_ordering_system
pipenv install


Migrate & Run Server
pipenv run python manage.py migrate
pipenv run python manage.py createsuperuser
pipenv run python manage.py runserver 0.0.0.0:8000



Demo Data
After creating a superuser, use the admin panel to:
Create Companies
Create Products (is_active=True)
Create Users assigned to companies with roles:
viewer (disabled order access)
operator (limited edit rights)
admin (full control)
You can also use the products-page and orders-page interfaces to simulate product/order creation.
Demo user examples:
admin_user / password123
operator_user / password123
viewer_user / password123


Endpoints refrences: 

/api/products/	GET / POST
/api/orders/	GET / POST
/api/orders/<id>/edit/	PATCH (restricted)
/api/orders/<id>/ship/	POST — marks as shipped and logs confirmation


Frontend pages:

Page	URL
Dashboard	    /dashboard/
Product Form & Listing	/products-page/
Order Form & Listing	/orders-page/


Admin Panel Actions:
    Login at /admin/
    Export selected orders to CSV
    Bulk deactivate products




---

## 🐳 Dockerized Setup

Prefer to run the project without local dependency hassles? This project comes fully Dockerized!

### 1. Configure environment variables

Create a `.env` file in the root directory with contents like:

```env
SECRET_KEY=your_secret_key
DEBUG=True
MYSQL_ROOT_PASSWORD=root
MYSQL_DATABASE=multi_tenant_db
MYSQL_USER=django_user
MYSQL_PASSWORD=123456



Run with Docker Compose:
  docker compose up --build