# eBipani

eBipani is a Django-based e-commerce platform designed to facilitate interactions between Customers, Sellers, and Administrators. It leverages an Oracle database (C##EBIPANI schema) for data storage and business logic, implemented via PL/SQL stored procedures, functions, and triggers.

## Project Overview

### Purpose
Provides a platform for users to browse products, manage shopping carts, place orders, leave reviews, and allow sellers to manage inventory, while administrators oversee users and shipping logistics.

### Key Features

- **User Authentication & Registration**: Register as Customer or Seller, login/logout, admin creation by existing admins. Uses a custom (insecure) password hashing function.
- **Product Catalog & Search**: Browse products by category, view details, search by keywords (name, category, sub-category).
- **Shopping Cart Management**: Add/update/remove items in a persistent cart (stored in SELECTS table), grouped by seller.
- **Order Placement & Processing**: Check stock, reserve items, simulate payment (Bkash), record orders, and allow seller approval with shipper assignment.
- **Product Review Management**: Customers rate/comment on purchased products; reviews displayed publicly.
- **Seller Product Management**: Sellers add/edit products, with automatic category creation.
- **User Profile Management**: Customers and Sellers update personal details and passwords.
- **Admin User Management**: Admins view/search/delete Customers/Sellers and create new Admins.
- **Admin Shipper Management**: Admins manage shippers (add/edit/delete) with unique postal codes.

### Technology Stack

- **Backend**: Django (Python)
- **Database**: Oracle (C##EBIPANI schema, PL/SQL)
- **Frontend**: Django templates (HTML, CSS, minimal JavaScript)
- **Database Connector**: cx_Oracle

### Architecture

The application follows a role-based architecture with distinct Django apps:
- eApp (main application)
- eAdmin
- eCustomer
- eSeller

The project uses raw SQL queries extensively over the Django ORM to interact with the database.

## Prerequisites

- Oracle Database installed and running
- Python 3.x installed
- Git (optional, for cloning the repository)

## Setup Instructions

### Step 1: Database Setup

1. **Install Oracle Database**:
   - Follow the Oracle installation guide to set up an Oracle instance.
   - Ensure the database is accessible on localhost:1521 with service name/SID orcl.

2. **Create the C##EBIPANI Schema**:
   - Run the `C##EBIPANI.sql` script in your Oracle SQL client (e.g., SQL*Plus or SQL Developer) to create the schema, tables, PL/SQL objects, and initial data.
   - Default credentials: Username: `c##eBipani`, Password: `eBipani`.

### Step 2: Python Environment Setup

1. **Install Django**:
   ```bash
   pip install django
   ```
   Refer to the [Django installation guide](https://docs.djangoproject.com/en/stable/topics/install/) for details.

2. **Install cx_Oracle**:
   ```bash
   pip install cx_oracle
   ```
   See the [cx_Oracle documentation](https://cx-oracle.readthedocs.io/en/latest/installation.html) for additional setup (e.g., Oracle client libraries).

3. **Verify Dependencies**:
   ```bash
   pip list
   ```
   Ensure both django and cx_oracle are listed.

### Step 3: Project Setup and Running

1. **Clone or Open the Project**:
   ```bash
   git clone <repository-url>
   cd eBipani
   ```
   Alternatively, extract the project files and open the directory in your terminal.

2. **Apply Django Migrations**:
   ```bash
   python manage.py migrate
   ```
   Note: The main schema is created via C##EBIPANI.sql, not migrations.

3. **Start the Development Server**:
   ```bash
   python manage.py runserver
   ```
   Access the site in your browser at http://127.0.0.1:8000/eApp/

## Usage

- **Public Access**: Browse products and search at `/eApp/`.
- **Customer Features**: 
  - Register at `/eApp/users/csignin/`
  - Login at `/eApp/users/login/`
  - Manage cart/orders at `/eApp/users/customer/`
- **Seller Features**: 
  - Register at `/eApp/users/ssignin/` 
  - Manage products/orders at `/eApp/users/seller/`
- **Admin Features**: 
  - Access admin tools at `/eApp/users/admin/` (requires Admin role)


## Potential Improvements

- Use Django ORM for simpler queries and schema management.
- Centralize static files to avoid duplication across apps.
- Enhance search with a dedicated engine (e.g., Elasticsearch) for scalability.
- Implement proper image upload/storage instead of relying on file paths.

## Troubleshooting

- **Database Connection Errors**: Verify Oracle is running, credentials match `settings.py` (`c##eBipani/eBipani@localhost:1521/orcl`), and cx_Oracle is correctly installed.
- **Server Not Starting**: Check for syntax errors or missing dependencies with `python manage.py check`.
- **404 Errors**: Ensure URLs are correctly prefixed with `/eApp/`.
