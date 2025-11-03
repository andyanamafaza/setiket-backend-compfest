# Setiket API Documentation

[![Django](https://img.shields.io/badge/Django-4.0-blue.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.14-red.svg)](https://www.django-rest-framework.org/)
[![Python](https://img.shields.io/badge/Python-3.8+-green.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Setiket** is a comprehensive event ticketing platform API built with Django REST Framework. It provides a complete solution for event organizers to create and manage events, and for customers to discover, purchase tickets, and manage their event registrations.

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [API Documentation](#-api-documentation)
  - [Authentication](#authentication)
  - [Customer Endpoints](#customer-endpoints)
  - [Event Organizer Endpoints](#event-organizer-endpoints)
  - [Admin Endpoints](#admin-endpoints)
- [Data Models](#-data-models)
- [Error Handling](#-error-handling)
- [Rate Limiting](#-rate-limiting)
- [Swagger Documentation](#-swagger-documentation)
- [Deployment](#-deployment)
- [Testing](#-testing)
- [User Roles & Permissions](#-user-roles--permissions)
- [API Endpoints Summary](#-api-endpoints-summary)
- [Contributing](#-contributing)

> 💡 **Tip:** Click on any section header to expand and view detailed information!

## ✨ Features

- 🔐 **JWT Authentication** - Secure token-based authentication with refresh tokens
- 👥 **Role-Based Access Control** - Three user roles: Customer, Event Organizer, and Administrator
- 🎫 **Event Management** - Create, update, and manage events with approval workflow
- 🎟️ **Ticket System** - Multiple ticket types (Free, Paid, Volunteer) with quantity management
- 💰 **Sales & Analytics** - Track sales data and analytics for event organizers
- 📧 **Email Notifications** - Automated email confirmations for ticket purchases
- 📸 **Image Upload** - SeaweedFS integration for event and profile images
- 🔍 **Event Discovery** - Advanced filtering, searching, and sorting capabilities
- 📊 **Admin Dashboard** - Complete admin interface for managing users and approving proposals
- 🔄 **Refund System** - Full refund processing with balance updates and email notifications
- 📱 **QR Code Generation** - Automatic QR code generation for tickets
- 🐳 **Docker Support** - Complete Docker setup for development and production
- 🔄 **CI/CD Pipeline** - Automated testing and deployment with GitHub Actions
- 🏥 **Health Monitoring** - Health check endpoint for load balancers and monitoring tools
- 🔒 **Rate Limiting** - Built-in rate limiting to prevent abuse
- 📝 **Code Quality** - Pre-commit hooks and code formatting tools

## 🛠 Tech Stack

- **Backend Framework**: Django 4.0+
- **API Framework**: Django REST Framework 3.14+
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Database**: PostgreSQL (via psycopg2-binary)
- **File Storage**: SeaweedFS (distributed file system)
- **API Documentation**: drf-spectacular (OpenAPI/Swagger)
- **Filtering**: django-filter for advanced filtering capabilities
- **QR Codes**: qrcode[pil] for ticket QR code generation
- **Deployment**: Docker, Docker Compose, Gunicorn
- **CI/CD**: GitHub Actions
- **Code Quality**: Black, isort, flake8, mypy
- **Other**: django-cors-headers, django-environ, whitenoise

## 📦 Prerequisites

### For Local Development
- Python 3.10 or higher
- PostgreSQL database
- SeaweedFS server (for file storage) - [Installation Guide](https://github.com/seaweedfs/seaweedfs)
- SMTP email server credentials (for email notifications)

### For Docker Development
- Docker and Docker Compose
- All prerequisites are handled automatically (including SeaweedFS)

## 🚀 Installation

### Option 1: Docker (Recommended)

<details>
<summary><b>🐳 Quick Start with Docker</b></summary>

```bash
# Clone the repository
git clone <repository-url>
cd setiket-backend-compfest

# Start services (development) - includes SeaweedFS
docker-compose -f docker-compose.dev.yml up --build

# Or for production-like setup
docker-compose up --build
```

The API will be available at `http://localhost:8000/api/`

**Note:** SeaweedFS is automatically started with Docker Compose for file storage.

</details>

### Option 2: Local Development

<details>
<summary><b>1. Clone the Repository</b></summary>

```bash
git clone <repository-url>
cd setiket-backend-compfest
```

</details>

<details>
<summary><b>2. Create Virtual Environment</b></summary>

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

</details>

<details>
<summary><b>3. Install Dependencies</b></summary>

```bash
pip install -r requirements.txt
```

</details>

<details>
<summary><b>4. Database Setup</b></summary>

```bash
cd backend
python manage.py migrate
python manage.py createsuperuser
```

</details>

<details>
<summary><b>5. Start SeaweedFS (Local Development)</b></summary>

For local development without Docker, you need to install and run SeaweedFS:

```bash
# Download SeaweedFS (example for Linux)
wget https://github.com/seaweedfs/seaweedfs/releases/latest/download/linux_amd64.tar.gz
tar -xzf linux_amd64.tar.gz

# Start SeaweedFS master
./weed master -ip=localhost -port=9333

# In another terminal, start volume server
./weed volume -dir=/tmp/seaweedfs -max=0 -mserver=localhost:9333 -port=8080

# In another terminal, start filer
./weed filer -master=localhost:9333 -port=8888
```

**Note:** With Docker, SeaweedFS is automatically started and configured.

</details>

<details>
<summary><b>6. Run Development Server</b></summary>

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`

</details>

## ⚙️ Configuration

<details>
<summary><b>Environment Variables Setup</b></summary>

Create a `.env` file in the `backend` directory with the following variables:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=postgresql://username:password@localhost:5432/dbname

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_SENDER=noreply@setiket.com
EMAIL_HOST_PASSWORD=your-app-password

# SeaweedFS (File Storage)
# For local development without Docker, install SeaweedFS separately
SEAWEEDFS_URL=http://localhost:8333
SEAWEEDFS_FILER_URL=http://localhost:8888
SEAWEEDFS_MASTER_URL=http://localhost:9333

# CORS (comma-separated list)

**Note:** For Docker, environment variables can be set in `.env` file or in `docker-compose.yml`.

</details>

## 📚 API Documentation

### Base URL

```
http://localhost:8000/api/v1
```

**Note:** The API is versioned. Both `/api/` and `/api/v1/` are supported for backward compatibility.

### Authentication

The API uses JWT (JSON Web Token) authentication. Most endpoints require authentication except for:
- Event listing (public)
- Event detail view (public)
- User registration

<details>
<summary><b>📝 Register User</b></summary>

#### Register User

```http
POST /api/auth/register/
Content-Type: application/json

{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "securepassword123",
  "phone_number": "+1234567890",
  "image": "<file>" // optional
}
```

**Response:**
```json
{
  "id": "uuid",
  "username": "johndoe",
  "email": "john@example.com",
  "balance": 1000000,
  "phone_number": "+1234567890",
  "image_url": "https://...",
  "role": "customer"
}
```

</details>

<details>
<summary><b>🔑 Login</b></summary>

#### Login

```http
POST /api/auth/login/
Content-Type: application/json

{
  "username": "johndoe",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

</details>

<details>
<summary><b>🔄 Refresh Token</b></summary>

#### Refresh Token

```http
POST /api/auth/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

</details>

<details>
<summary><b>🚪 Logout</b></summary>

#### Logout

```http
POST /api/auth/logout/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Using Authentication

Include the access token in the Authorization header:

```http
Authorization: Bearer <access_token>
```

</details>

---

## 👤 Customer Endpoints

<details>
<summary><b>📋 List Events</b></summary>

### List Events

Retrieve all approved events with advanced filtering, searching, and sorting.

```http
GET /api/v1/event/?category=seminar&city=Jakarta&min_price=50000&ordering=-start_date&search=tech
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `category` (optional): Filter by category (`seminar`, `konser`, `horror`, `komedi`, `olahraga`)
- `city` (optional): Filter by city (partial match)
- `start_date_from` (optional): Filter events starting from this date (YYYY-MM-DD)
- `start_date_to` (optional): Filter events starting until this date (YYYY-MM-DD)
- `min_price` (optional): Minimum ticket price
- `max_price` (optional): Maximum ticket price
- `search` (optional): Search in title, description, city, place_name
- `ordering` (optional): Sort by field (e.g., `start_date`, `-created_at`, `city,-start_date`)

**Response:**
```json
[
  {
    "id": "uuid",
    "title": "Tech Conference 2024",
    "image_url": "https://...",
    "start_date": "2024-06-01",
    "end_date": "2024-06-02",
    "start_time": "09:00:00",
    "end_time": "17:00:00",
    "city": "Jakarta",
    "price": 150000,
    "category": "seminar",
    "organizer": "organizer_username",
    "url_detail": "http://localhost:8000/api/event/{id}/",
    "is_online": false
  }
]
```

</details>

<details>
<summary><b>🔍 Get Event Details</b></summary>

### Get Event Details

```http
GET /api/event/{id}/
Authorization: Bearer <access_token> (optional)
```

**Response:**
```json
{
  "title": "Tech Conference 2024",
  "image_url": "https://...",
  "description": "Annual tech conference...",
  "start_date": "2024-06-01",
  "end_date": "2024-06-02",
  "start_time": "09:00:00",
  "end_time": "17:00:00",
  "place_name": "Jakarta Convention Center",
  "city": "Jakarta",
  "full_address": "Jl. Gatot Subroto...",
  "location": "Jakarta Convention Center",
  "category": "seminar",
  "organizer": "organizer_username",
  "ticket_type": [
    {
      "id": "uuid",
      "title": "VIP Ticket",
      "start_date": "2024-06-01",
      "end_date": "2024-06-02",
      "start_time": "09:00:00",
      "end_time": "17:00:00",
      "ticket_quantity": 100,
      "ticket_type": "paid",
      "description": "VIP access",
      "price": "150000.00"
    }
  ]
}
```

</details>

<details>
<summary><b>📅 Get Upcoming Events</b></summary>

### Get Upcoming Events

Get events where the user has purchased tickets.

```http
GET /api/event/upcoming/
Authorization: Bearer <access_token>
```

**Response:** Same as List Events

</details>

<details>
<summary><b>🎟️ Purchase Ticket</b></summary>

### Purchase Ticket

```http
POST /api/v1/ticket/purchase/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "ticket_id": "uuid",
  "price": 150000  // Required for "relawan" ticket type
}
```

**Response:**
```json
{
  "id": "uuid",
  "owner": "johndoe",
  "title": "VIP Ticket",
  "event": "Tech Conference 2024",
  "start_date": "2024-06-01",
  "end_date": "2024-06-02",
  "start_time": "09:00:00",
  "end_time": "17:00:00",
  "ticket_type": "paid",
  "price": "150000.00"
}
```

**Note:** 
- An email confirmation will be sent to the user's email address
- A QR code is automatically generated and stored with the ticket

</details>

<details>
<summary><b>🔄 Refund Ticket</b></summary>

### Refund Ticket

Refund a purchased ticket. Only the ticket owner can request a refund.

```http
DELETE /api/v1/ticket/{id}/refund/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "reason": "Event cancelled"  // Optional
}
```

**Response:**
```json
{
  "message": "Ticket refunded successfully. The amount has been added to your balance."
}
```

**Note:** 
- Cannot refund tickets for past events
- Refund amount is added back to user balance
- Ticket quantity is restored
- Email confirmation is sent

</details>

<details>
<summary><b>📱 Get Ticket QR Code</b></summary>

### Get Ticket QR Code

Retrieve the QR code for a purchased ticket.

```http
GET /api/v1/ticket/{id}/qr/
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "qr_code": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...",
  "qr_code_string": "SETIKET-{ticket-id}",
  "ticket_id": "uuid",
  "event": "Tech Conference 2024",
  "ticket": "VIP Ticket"
}
```

**Note:** QR code is automatically generated when ticket is purchased.

</details>

<details>
<summary><b>👤 Get/Update Account</b></summary>

### Get/Update Account

```http
GET /api/account/
Authorization: Bearer <access_token>
```

```http
PATCH /api/account/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "username": "newusername",
  "email": "newemail@example.com",
  "phone_number": "+1234567890",
  "password": "newpassword123",
  "image": "<file>"
}
```

**Response:**
```json
{
  "id": "uuid",
  "username": "johndoe",
  "email": "john@example.com",
  "phone_number": "+1234567890",
  "image_url": "https://...",
  "role": "customer"
}
```

</details>

---

## 🎪 Event Organizer Endpoints

<details>
<summary><b>➕ Create Event</b></summary>

### Create Event

```http
POST /api/event-organizer/event/create/
Authorization: Bearer <access_token>
Content-Type: multipart/form-data

{
  "title": "Tech Conference 2024",
  "image": "<file>",
  "description": "Annual tech conference...",
  "start_date": "2024-06-01",
  "end_date": "2024-06-02",
  "start_time": "09:00:00",
  "end_time": "17:00:00",
  "place_name": "Jakarta Convention Center",
  "city": "Jakarta",
  "full_address": "Jl. Gatot Subroto...",
  "location": "Jakarta Convention Center",
  "category": "seminar",
  "is_online": false
}
```

**Response:**
```json
{
  "id": "uuid",
  "title": "Tech Conference 2024",
  "image_url": "https://...",
  "description": "Annual tech conference...",
  "start_date": "2024-06-01",
  "end_date": "2024-06-02",
  "start_time": "09:00:00",
  "end_time": "17:00:00",
  "place_name": "Jakarta Convention Center",
  "city": "Jakarta",
  "full_address": "Jl. Gatot Subroto...",
  "location": "Jakarta Convention Center",
  "category": "seminar",
  "status": "pending",
  "message": "",
  "owner": "organizer_username",
  "registered_users_url": "http://localhost:8000/api/event-users/{id}/"
}
```

**Note:** Event status will be `pending` until approved by an administrator.

</details>

<details>
<summary><b>✏️ Update Event</b></summary>

### Update Event

```http
PATCH /api/event-organizer/event/update/{id}/
Authorization: Bearer <access_token>
Content-Type: multipart/form-data

{
  "title": "Updated Event Title",
  "description": "Updated description...",
  // ... other fields
}
```

</details>

<details>
<summary><b>📋 List Own Events</b></summary>

### List Own Events

```http
GET /api/event-organizer/ownevent/
Authorization: Bearer <access_token>
```

**Response:** Array of event objects (same structure as Create Event)

</details>

<details>
<summary><b>📊 Get Sales Data</b></summary>

### Get Sales Data

```http
GET /api/event-organizer/sales-data/
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "total_sales": 5000000.00,
  "total_active_event": 5,
  "total_sold_ticket": 150,
  "event_data": [
    {
      "title": "Tech Conference 2024",
      "status": false,
      "total_sales": 2000000.00,
      "total_sold": 50
    }
  ]
}
```

</details>

<details>
<summary><b>👥 Get Registered Users for Event</b></summary>

### Get Registered Users for Event

```http
GET /api/event-users/{event_id}/
Authorization: Bearer <access_token>
```

**Response:**
```json
[
  {
    "id": "uuid",
    "customer_username": "johndoe",
    "costumer_email": "john@example.com",
    "ticket_type": "paid",
    "price": "150000.00",
    "event": "Tech Conference 2024",
    "created_at": "2024-05-15T10:30:00Z"
  }
]
```

</details>

<details>
<summary><b>🎫 Create Ticket</b></summary>

### Create Ticket

```http
POST /api/ticket/create/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "title": "VIP Ticket",
  "event_id": "uuid",
  "start_date": "2024-06-01",
  "end_date": "2024-06-02",
  "start_time": "09:00:00",
  "end_time": "17:00:00",
  "ticket_quantity": 100,
  "ticket_type": "paid",  // "free", "relawan", or "paid"
  "description": "VIP access with premium benefits",
  "price": 150000  // Required for "paid" and "relawan" types
}
```

**Response:**
```json
{
  "id": "uuid",
  "title": "VIP Ticket",
  "event_id": "uuid",
  "start_date": "2024-06-01",
  "end_date": "2024-06-02",
  "start_time": "09:00:00",
  "end_time": "17:00:00",
  "ticket_quantity": 100,
  "ticket_type": "paid",
  "description": "VIP access with premium benefits",
  "price": "150000.00"
}
```

**Ticket Type Rules:**
- `free`: Price must be 0
- `paid`: Price is required and must be > 0
- `relawan`: Price is required (minimum price), customers can pay more

</details>

<details>
<summary><b>📝 Event Organizer Proposal</b></summary>

### Event Organizer Proposal

<details>
<summary><b>➕ Create Proposal</b></summary>

#### Create Proposal

Users can submit a proposal to become an event organizer.

```http
POST /api/event-organizer-proposal/create/
Authorization: Bearer <access_token>
Content-Type: multipart/form-data

{
  "name": "My Event Company",
  "category": "entertainment",
  "description": "We organize various entertainment events...",
  "location": "Jakarta, Indonesia",
  "banner": "<file>",
  "proposal": "<file>"
}
```

</details>

<details>
<summary><b>📋 List Own Proposals</b></summary>

#### List Own Proposals

```http
GET /api/event-organizer-proposal/
Authorization: Bearer <access_token>
```

</details>

<details>
<summary><b>🔍 Get Proposal Details</b></summary>

#### Get Proposal Details

```http
GET /api/event-organizer-proposal/{id}/
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "id": "uuid",
  "name": "My Event Company",
  "banner_url": "https://...",
  "proposal_url": "https://...",
  "description": "We organize various entertainment events...",
  "location": "Jakarta, Indonesia",
  "category": "entertainment",
  "status": "pending",
  "message": "",
  "owner": "username",
  "url_detail": "http://localhost:8000/api/event-organizer-proposal/{id}/"
}
```

</details>

</details>

---

## 👑 Admin Endpoints

**All admin endpoints require administrator role.**

<details>
<summary><b>👥 List All Users</b></summary>

### List All Users

```http
GET /api/admin/user-list/
Authorization: Bearer <access_token>
```

**Response:**
```json
[
  {
    "id": "uuid",
    "username": "johndoe",
    "email": "john@example.com",
    "role": "customer"
  }
]
```

</details>

<details>
<summary><b>🎪 List Event Organizers</b></summary>

### List Event Organizers

```http
GET /api/admin/event-organizers-list/
Authorization: Bearer <access_token>
```

**Response:**
```json
[
  {
    "id": "uuid",
    "username": "organizer1",
    "email": "org@example.com",
    "event_url": "http://localhost:8000/api/admin/event-organizers/{id}/events/"
  }
]
```

</details>

<details>
<summary><b>📋 Get Events by Organizer</b></summary>

### Get Events by Organizer

```http
GET /api/admin/event-organizers/{organizer_id}/events/
Authorization: Bearer <access_token>
```

</details>

<details>
<summary><b>✅ Event Proposals Management</b></summary>

### Event Proposals Management

<details>
<summary><b>📋 List Event Proposals</b></summary>

#### List Event Proposals

```http
GET /api/admin/event-proposals/
Authorization: Bearer <access_token>
```

**Response:**
```json
[
  {
    "id": "uuid",
    "title": "New Event Proposal",
    "created_at": "2024-05-15T10:30:00Z",
    "event_confirmation_url": "http://localhost:8000/api/admin/event-proposals/{id}/confirm/",
    "event_proposal_detail_url": "http://localhost:8000/api/admin/event-proposals/{id}/"
  }
]
```

</details>

<details>
<summary><b>🔍 Get Event Proposal Details</b></summary>

#### Get Event Proposal Details

```http
GET /api/admin/event-proposals/{id}/
Authorization: Bearer <access_token>
```

</details>

<details>
<summary><b>✅ Approve/Reject Event Proposal</b></summary>

#### Approve/Reject Event Proposal

```http
PATCH /api/admin/event-proposals/{id}/confirm/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "status": "approved",  // or "rejected"
  "message": "Event approved successfully"
}
```

</details>

</details>

<details>
<summary><b>👤 Event Organizer Proposals Management</b></summary>

### Event Organizer Proposals Management

<details>
<summary><b>📋 List Event Organizer Proposals</b></summary>

#### List Event Organizer Proposals

```http
GET /api/admin/event-organizer-proposals/
Authorization: Bearer <access_token>
```

**Response:**
```json
[
  {
    "id": "uuid",
    "organizer": "username",
    "name": "My Event Company",
    "created_at": "2024-05-15T10:30:00Z",
    "event_organizer_confirmation_url": "http://localhost:8000/api/admin/event-organizer-proposals/{id}/confirm/",
    "event_organizer_proposal_detail_url": "http://localhost:8000/api/admin/event-organizer-proposals/{id}/"
  }
]
```

</details>

<details>
<summary><b>🔍 Get Event Organizer Proposal Details</b></summary>

#### Get Event Organizer Proposal Details

```http
GET /api/admin/event-organizer-proposals/{id}/
Authorization: Bearer <access_token>
```

</details>

<details>
<summary><b>✅ Approve/Reject Event Organizer Proposal</b></summary>

#### Approve/Reject Event Organizer Proposal

```http
PATCH /api/admin/event-organizer-proposals/{id}/confirm/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "status": "approved",  // or "rejected"
  "message": "Proposal approved. User role updated to event_organizer."
}
```

**Note:** When approved, the user's role is automatically updated to `event_organizer`.

</details>

</details>

<details>
<summary><b>✏️ Update User Account (Admin)</b></summary>

### Update User Account (Admin)

```http
PATCH /api/account/{user_id}/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "username": "newusername",
  "email": "newemail@example.com",
  "phone_number": "+1234567890",
  "password": "newpassword123",
  "image": "<file>"
}
```

</details>

---

## 📊 Data Models

<details>
<summary><b>👤 User Model</b></summary>

### User

| Field | Type | Description |
|-------|------|-------------|
| `id` | UUID | Primary key |
| `username` | String | Unique username |
| `email` | String | Unique email address |
| `password` | String | Hashed password |
| `balance` | Integer | User balance (default: 1,000,000) |
| `phone_number` | String | Phone number (optional) |
| `image` | ImageField | Profile image (optional, stored in SeaweedFS) |
| `role` | String | User role: `customer`, `event_organizer`, `administrator` |
| `created_at` | DateTime | Account creation timestamp |

</details>

<details>
<summary><b>🎪 Event Model</b></summary>

### Event

| Field | Type | Description |
|-------|------|-------------|
| `id` | UUID | Primary key |
| `title` | String | Event title |
| `image` | ImageField | Event banner image (stored in SeaweedFS) |
| `description` | Text | Event description |
| `start_date` | Date | Event start date |
| `end_date` | Date | Event end date |
| `start_time` | Time | Event start time |
| `end_time` | Time | Event end time |
| `place_name` | String | Venue name |
| `city` | String | City name |
| `full_address` | Text | Full address |
| `location` | Text | Location details |
| `category` | String | Category: `seminar`, `konser`, `horror`, `komedi`, `olahraga` |
| `status` | String | Status: `pending`, `approved`, `rejected` |
| `message` | Text | Admin message (for approval/rejection) |
| `is_online` | Boolean | Whether event is online |
| `total_sold` | Integer | Total tickets sold |
| `total_sales` | Decimal | Total sales amount |
| `organizer` | ForeignKey | Reference to User (event organizer) |
| `created_at` | DateTime | Creation timestamp |

</details>

<details>
<summary><b>🎫 Ticket Model</b></summary>

### Ticket

| Field | Type | Description |
|-------|------|-------------|
| `id` | UUID | Primary key |
| `title` | String | Ticket name |
| `event` | ForeignKey | Reference to Event |
| `start_date` | Date | Ticket sale start date |
| `end_date` | Date | Ticket sale end date |
| `start_time` | Time | Ticket sale start time |
| `end_time` | Time | Ticket sale end time |
| `ticket_quantity` | Integer | Available ticket quantity |
| `ticket_type` | String | Type: `free`, `relawan`, `paid` |
| `description` | Text | Ticket description |
| `price` | Decimal | Ticket price |
| `created_at` | DateTime | Creation timestamp |

</details>

<details>
<summary><b>🎟️ UserTicket Model</b></summary>

### UserTicket

| Field | Type | Description |
|-------|------|-------------|
| `id` | UUID | Primary key |
| `customer` | ForeignKey | Reference to User (customer) |
| `ticket` | ForeignKey | Reference to Ticket |
| `event` | ForeignKey | Reference to Event |
| `price` | Decimal | Purchase price |
| `sales_data` | ForeignKey | Reference to SalesData |
| `qr_code` | String | QR code string for ticket verification |
| `created_at` | DateTime | Purchase timestamp |
| `updated_at` | DateTime | Last update timestamp |

</details>

<details>
<summary><b>📝 EventOrganizerProposal Model</b></summary>

### EventOrganizerProposal

| Field | Type | Description |
|-------|------|-------------|
| `id` | UUID | Primary key |
| `organizer` | ForeignKey | Reference to User |
| `name` | String | Company/organization name |
| `category` | String | Category of events |
| `description` | Text | Proposal description |
| `location` | Text | Location |
| `banner` | ImageField | Banner image (stored in SeaweedFS) |
| `proposal` | FileField | Proposal document/image (stored in SeaweedFS) |
| `status` | String | Status: `pending`, `approved`, `rejected` |
| `message` | Text | Admin message |
| `created_at` | DateTime | Submission timestamp |

</details>

<details>
<summary><b>💰 SalesData Model</b></summary>

### SalesData

| Field | Type | Description |
|-------|------|-------------|
| `id` | UUID | Primary key |
| `event` | ForeignKey | Reference to Event |
| `organizer` | ForeignKey | Reference to User (organizer) |
| `amount` | Decimal | Total sales amount |
| `created_at` | DateTime | Creation timestamp |

</details>

---

## ⚠️ Error Handling

The API uses standard HTTP status codes:

| Status Code | Description |
|-------------|-------------|
| `200` | OK - Request successful |
| `201` | Created - Resource created successfully |
| `205` | Reset Content - Logout successful |
| `400` | Bad Request - Invalid request data |
| `401` | Unauthorized - Authentication required |
| `403` | Forbidden - Insufficient permissions |
| `404` | Not Found - Resource not found |
| `500` | Internal Server Error - Server error |

<details>
<summary><b>📋 Error Response Format</b></summary>

### Error Response Format

```json
{
  "detail": "Error message here",
  "field_name": ["Field-specific error message"]
}
```

</details>

<details>
<summary><b>🔍 Common Error Scenarios</b></summary>

### Common Error Scenarios

1. **Invalid Credentials**
   ```json
   {
     "detail": "No active account found with the given credentials"
   }
   ```

2. **Insufficient Permissions**
   ```json
   {
     "detail": "Insufficient role permissions."
   }
   ```

3. **Validation Error**
   ```json
   {
     "price": ["Price must be greater or equal than 0"]
   }
   ```

4. **Resource Not Found**
   ```json
   {
     "detail": "Not found."
   }
   ```

</details>

---

## 🔒 Rate Limiting

Rate limiting is implemented using Django REST Framework throttling:

- **Anonymous users**: 100 requests per hour
- **Authenticated users**: 1000 requests per hour

Rate limits can be customized in `backend/backend/settings.py`.

---

## 📖 API Documentation

### Swagger/OpenAPI Documentation

Interactive API documentation is available at:

```
http://localhost:8000/api/docs/
http://localhost:8000/apidocs/  (legacy)
```

API schema (OpenAPI 3.0) is available at:

```
http://localhost:8000/api/schema/
```

## 🏥 Health Check

The API includes a health check endpoint for monitoring:

```http
GET /api/v1/health/
```

**Response:**
```json
{
  "status": "healthy",
  "database": "connected",
  "version": "1.0.0"
}
```

Returns HTTP 200 if healthy, HTTP 503 if unhealthy.

---

## 🚀 Deployment

<details>
<summary><b>🐳 Docker Deployment (Recommended)</b></summary>

### Docker Deployment

```bash
# Production deployment
docker-compose -f docker-compose.prod.yml up --build -d

# Run migrations
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate

# Collect static files
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput
```

</details>

<details>
<summary><b>🐳 Detailed Docker Guide</b></summary>

### Docker Compose Files

- `docker-compose.yml` - Default (production-like)
- `docker-compose.dev.yml` - Development (with hot reload)
- `docker-compose.prod.yml` - Production optimized

### Building Docker Image

```bash
docker build -t setiket-backend .
```

### Running Migrations

```bash
# Development
docker-compose -f docker-compose.dev.yml exec web python manage.py migrate

# Production
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
```

### Collecting Static Files

```bash
docker-compose exec web python manage.py collectstatic --noinput
```

### Docker Volumes

- `postgres_data` - PostgreSQL database data
- `static_volume` - Static files
- `media_volume` - Media files
- `logs_volume` - Application logs
- `seaweedfs_data` - SeaweedFS file storage data

### Troubleshooting

**Database Connection Issues:**
```bash
# Check if database is ready
docker-compose ps

# View database logs
docker-compose logs db

# Access database shell
docker-compose exec db psql -U setiket_user -d setiket_db
```

**SeaweedFS Connection Issues:**
```bash
# Check SeaweedFS status
docker-compose logs seaweedfs

# Check SeaweedFS master status
curl http://localhost:9333/dir/status

# Check SeaweedFS filer status
curl http://localhost:8888/status
```

**Container Issues:**
```bash
# View logs
docker-compose logs web

# Restart services
docker-compose restart

# Rebuild containers
docker-compose up --build
```

</details>

<details>
<summary><b>✅ Production Checklist</b></summary>

### Production Checklist

1. **Environment Variables**
   - Set `DEBUG=False`
   - Use strong `SECRET_KEY`
   - Configure `ALLOWED_HOSTS`
   - Set up production database
   - Configure email settings
   - Set `CORS_ALLOWED_ORIGINS` for production domains

2. **Static Files**
   ```bash
   python manage.py collectstatic
   ```

3. **Database Migrations**
   ```bash
   python manage.py migrate
   ```

4. **Run with Gunicorn**
   ```bash
   cd backend
   gunicorn backend.wsgi:application --bind 0.0.0.0:8000 --workers 4
   ```

5. **Health Check**
   - Verify health endpoint: `GET /api/v1/health/`
   - Set up monitoring tools

</details>

<details>
<summary><b>⚙️ Environment Variables for Production</b></summary>

### Environment Variables for Production

```env
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:password@host:5432/dbname

# SeaweedFS (File Storage)
SEAWEEDFS_URL=http://seaweedfs:8333
SEAWEEDFS_FILER_URL=http://seaweedfs:8888
SEAWEEDFS_MASTER_URL=http://seaweedfs:9333

# Email
EMAIL_HOST=smtp.your-provider.com
EMAIL_HOST_USER=your-email@domain.com
EMAIL_HOST_SENDER=noreply@yourdomain.com
EMAIL_HOST_PASSWORD=your-email-password

# CORS
CORS_ALLOWED_ORIGINS=https://your-frontend.com,https://www.your-frontend.com
```

</details>

<details>
<summary><b>🔄 CI/CD Pipeline</b></summary>

### CI/CD with GitHub Actions

The project includes a GitHub Actions workflow (`.github/workflows/ci.yml`) that:
- Runs tests on push/PR
- Performs code quality checks (Black, isort, flake8)
- Builds Docker images
- Can deploy to production (configure deployment steps)

To set up CI/CD:
1. Add `DOCKER_USERNAME` and `DOCKER_PASSWORD` to GitHub Secrets
2. Configure deployment steps in the workflow file

</details>

---

## 🏗️ Architecture

<details>
<summary><b>📐 System Architecture Overview</b></summary>

### Project Structure

```
backend/
├── api/                    # Main application
│   ├── models.py          # Database models
│   ├── views.py           # API views
│   ├── serializers.py     # DRF serializers
│   ├── urls.py            # URL routing
│   ├── permissions.py     # Custom permissions
│   ├── filters.py         # Filter sets
│   ├── services.py       # Business logic layer
│   ├── storage.py        # SeaweedFS storage backend
│   ├── health.py         # Health check endpoint
│   ├── qr_code.py        # QR code generation
│   ├── qr_code_views.py  # QR code endpoints
│   └── refund_views.py    # Refund endpoints
├── backend/               # Django project settings
│   ├── settings.py        # Django settings
│   ├── urls.py            # Root URL config
│   ├── wsgi.py            # WSGI config
│   └── asgi.py            # ASGI config
└── manage.py              # Django management script
```

### Key Components

**Models:**
1. **User** - Custom user model with roles (customer, event_organizer, administrator)
2. **Event** - Event information with approval workflow
3. **Ticket** - Ticket types and pricing
4. **UserTicket** - Purchased tickets with QR codes
5. **EventOrganizerProposal** - Proposal system for becoming an organizer
6. **SalesData** - Sales statistics per event

**Services Layer:**
- **TicketPurchaseService** - Handles ticket purchases atomically
- **RefundService** - Handles ticket refunds
- **QRCodeService** - Generates QR codes for tickets

**Security Features:**
1. JWT Authentication - Token-based authentication
2. Role-Based Access Control - Custom permissions
3. CORS Configuration - Restricted origins
4. Rate Limiting - DRF throttling
5. Password Validation - Django password validators
6. SQL Injection Protection - Django ORM

**Database Optimizations:**
1. Indexes - On frequently queried fields
2. Composite Indexes - For common query patterns
3. select_related - For foreign key relationships
4. prefetch_related - For reverse foreign keys

</details>

<details>
<summary><b>🔄 CI/CD Pipeline Details</b></summary>

### GitHub Actions Workflow

The project includes a GitHub Actions workflow (`.github/workflows/ci.yml`) that:

**Testing:**
- Runs tests on push/PR
- PostgreSQL service for testing
- Automated migrations

**Code Quality:**
- Black formatting check
- isort import sorting check
- flake8 linting check

**Build & Deploy:**
- Docker image building
- Docker image pushing to registry
- Deployment ready (configure deployment steps)

**Setup Requirements:**
1. Add `DOCKER_USERNAME` and `DOCKER_PASSWORD` to GitHub Secrets
2. Configure deployment steps in the workflow file

</details>

<details>
<summary><b>📊 Recent Improvements Summary</b></summary>

### Completed Implementations

**1. DevOps (Docker, CI/CD) ✅**
- Production-ready Dockerfile
- Docker Compose files (dev, prod, default)
- GitHub Actions CI/CD pipeline
- Automated testing and code quality checks

**2. Features ✅**
- **Refund System**: Atomic refund processing with balance updates
- **QR Code Generation**: Automatic QR codes for tickets
- **Payment Integration**: Ready for gateway integration (Midtrans, Xendit, Stripe)

**3. Monitoring ✅**
- Health check endpoint (`/api/v1/health/`)
- Structured logging configured
- Error tracking ready (can integrate Sentry)

**4. Code Maintenance ✅**
- Black code formatting
- isort import sorting
- flake8 linting
- Pre-commit hooks configured
- mypy type checking (optional)

**5. Database Optimizations ✅**
- Indexes on frequently queried fields
- Composite indexes for common queries
- N+1 query optimizations
- Efficient aggregations

**6. Security Enhancements ✅**
- Rate limiting (100/hour anonymous, 1000/hour authenticated)
- CORS restricted to specific origins
- Password validation
- JWT-only authentication in production

**7. API Improvements ✅**
- Advanced filtering, searching, sorting
- API versioning (v1)
- Pagination (20 items per page)
- Comprehensive error handling

</details>

---

## 🧪 Testing

### Running Tests

```bash
# Local testing
cd backend
python manage.py test

# Docker testing
docker-compose exec web python manage.py test
```

### Code Quality Checks

```bash
# Format code
black backend/

# Sort imports
isort backend/

# Lint
flake8 backend/

# Type check (optional)
mypy backend/
```

### Pre-commit Hooks

Install pre-commit hooks for automatic code quality checks:

```bash
pip install pre-commit
pre-commit install
```

### Example Test Scripts

Test scripts are available in the `apitesting/` directory for manual API testing.

---

## 👥 User Roles & Permissions

<details>
<summary><b>👤 Customer Permissions</b></summary>

### Customer
- Register and manage account
- Browse and view events
- Purchase tickets
- View upcoming events

</details>

<details>
<summary><b>🎪 Event Organizer Permissions</b></summary>

### Event Organizer
- All customer permissions
- Create and manage events
- Create tickets
- View sales data
- View registered users for events
- Submit event organizer proposals

</details>

<details>
<summary><b>👑 Administrator Permissions</b></summary>

### Administrator
- All permissions
- Approve/reject events
- Approve/reject event organizer proposals
- View all users and event organizers
- Manage user accounts

</details>

---

## 📝 API Endpoints Summary

<details>
<summary><b>📋 View Complete Endpoints Table</b></summary>

| Method | Endpoint | Auth | Role | Description |
|--------|----------|------|------|-------------|
| POST | `/api/v1/auth/register/` | No | - | Register new user |
| POST | `/api/v1/auth/login/` | No | - | Login and get tokens |
| POST | `/api/v1/auth/refresh/` | No | - | Refresh access token |
| POST | `/api/v1/auth/logout/` | Yes | Any | Logout user |
| GET | `/api/v1/event/` | Yes | Customer/Admin | List events |
| GET | `/api/v1/event/{id}/` | Optional | - | Get event details |
| GET | `/api/v1/event/upcoming/` | Yes | Customer/Admin | Get upcoming events |
| POST | `/api/v1/ticket/purchase/` | Yes | Customer/Admin | Purchase ticket |
| DELETE | `/api/v1/ticket/{id}/refund/` | Yes | Owner | Refund ticket |
| GET | `/api/v1/ticket/{id}/qr/` | Yes | Owner | Get ticket QR code |
| GET | `/api/v1/health/` | No | - | Health check |
| GET | `/api/v1/account/` | Yes | Any | Get own account |
| PATCH | `/api/v1/account/` | Yes | Any | Update own account |
| POST | `/api/v1/event-organizer/event/create/` | Yes | Organizer/Admin | Create event |
| PATCH | `/api/v1/event-organizer/event/update/{id}/` | Yes | Owner/Admin | Update event |
| GET | `/api/v1/event-organizer/ownevent/` | Yes | Organizer/Admin | List own events |
| GET | `/api/v1/event-organizer/sales-data/` | Yes | Organizer/Admin | Get sales data |
| GET | `/api/v1/event-users/{id}/` | Yes | Organizer/Admin | Get registered users |
| POST | `/api/v1/ticket/create/` | Yes | Organizer/Admin | Create ticket |
| POST | `/api/v1/event-organizer-proposal/create/` | Yes | Any | Create organizer proposal |
| GET | `/api/v1/event-organizer-proposal/` | Yes | Organizer/Admin | List own proposals |
| GET | `/api/v1/event-organizer-proposal/{id}/` | Yes | Organizer/Admin | Get proposal details |
| GET | `/api/v1/admin/user-list/` | Yes | Admin | List all users |
| GET | `/api/v1/admin/event-organizers-list/` | Yes | Admin | List organizers |
| GET | `/api/v1/admin/event-organizers/{id}/events/` | Yes | Admin | Get organizer events |
| GET | `/api/v1/admin/event-proposals/` | Yes | Admin | List event proposals |
| GET | `/api/v1/admin/event-proposals/{id}/` | Yes | Admin | Get event proposal |
| PATCH | `/api/v1/admin/event-proposals/{id}/confirm/` | Yes | Admin | Approve/reject event |
| GET | `/api/v1/admin/event-organizer-proposals/` | Yes | Admin | List organizer proposals |
| GET | `/api/v1/admin/event-organizer-proposals/{id}/` | Yes | Admin | Get organizer proposal |
| PATCH | `/api/v1/admin/event-organizer-proposals/{id}/confirm/` | Yes | Admin | Approve/reject proposal |
| DELETE | `/api/v1/admin/ticket/{id}/refund/` | Yes | Admin | Admin refund ticket |
| PATCH | `/api/v1/account/{id}/` | Yes | Admin | Update user account |

</details>

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Code Style

- Follow PEP 8 for Python code
- Use Django REST Framework conventions
- Write docstrings for functions and classes
- Add comments for complex logic
- Code is automatically formatted with Black and isort
- Pre-commit hooks ensure code quality

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🎯 Version History

- **v1.0.0** - Initial release
  - User authentication with JWT
  - Event management
  - Ticket system
  - Admin dashboard
  - Email notifications

- **v1.1.0** - Major improvements
  - ✨ Refund system with atomic transactions
  - 📱 QR code generation for tickets
  - 🐳 Docker support (development and production)
  - 🔄 CI/CD pipeline with GitHub Actions
  - 🏥 Health check endpoint
  - 🔍 Advanced filtering, searching, and sorting
  - 📊 Database optimizations (indexes, query optimization)
  - 🔒 Enhanced security (rate limiting, CORS configuration)
  - 📝 Code quality tools (Black, isort, flake8, pre-commit hooks)
  - 📚 Comprehensive documentation

- **v1.2.0** - File Storage Migration
  - 🗄️ **SeaweedFS Integration** - Replaced Cloudinary with SeaweedFS for distributed file storage
  - 🐳 SeaweedFS service added to Docker Compose
  - 📦 Custom SeaweedFS storage backend implementation
  - 🔧 Updated all file upload fields to use SeaweedFS

