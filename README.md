# Setiket API Documentation

[![Django](https://img.shields.io/badge/Django-4.0-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.14-blue.svg)](https://www.django-rest-framework.org/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A comprehensive Event Management and Ticketing API built with Django REST Framework. This API enables customers to browse events, purchase tickets, and allows event organizers to create and manage events with administrative oversight.

## ?? Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Authentication](#authentication)
- [API Endpoints](#api-endpoints)
- [Request/Response Examples](#requestresponse-examples)
- [Error Handling](#error-handling)
- [Data Models](#data-models)
- [Testing](#testing)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## ?? Overview

Setiket is a RESTful API for managing events and ticket sales. The system supports three user roles:

- **Customer**: Browse events, purchase tickets, manage account
- **Event Organizer**: Create events, manage tickets, view sales data
- **Administrator**: Manage users, approve/reject events and organizer proposals

## ? Features

- ?? JWT-based authentication with refresh tokens
- ?? Event management with multi-category support
- ?? Ticket purchase system with balance management
- ?? Sales analytics and reporting
- ?? User role management (Customer, Event Organizer, Administrator)
- ?? Email confirmation for ticket purchases
- ??? Cloudinary integration for image storage
- ?? Event proposal system for organizers
- ?? Event filtering by category
- ?? Real-time sales tracking

## ??? Tech Stack

- **Backend Framework**: Django 4.0
- **API Framework**: Django REST Framework
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Database**: PostgreSQL (via dj-database-url)
- **Image Storage**: Cloudinary
- **API Documentation**: drf-spectacular (Swagger/OpenAPI)
- **Deployment**: Gunicorn + Uvicorn
- **CORS**: django-cors-headers
- **Static Files**: WhiteNoise

## ?? Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.8 or higher
- PostgreSQL 12 or higher
- pip (Python package manager)
- Git

## ?? Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
cd backend
pip install -r ../requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the `backend` directory:

```bash
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_SENDER=noreply@setiket.com
EMAIL_HOST_PASSWORD=your-email-password
```

### 5. Run Migrations

```bash
python manage.py migrate
```

### 6. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 7. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### 8. Run Development Server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`

## ?? Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SECRET_KEY` | Django secret key | Yes |
| `DEBUG` | Debug mode (True/False) | Yes |
| `ALLOWED_HOSTS` | Comma-separated list of allowed hosts | Yes |
| `DATABASE_URL` | PostgreSQL connection string | Yes |
| `EMAIL_HOST` | SMTP server host | Yes |
| `EMAIL_HOST_USER` | SMTP username | Yes |
| `EMAIL_HOST_SENDER` | Email sender address | Yes |
| `EMAIL_HOST_PASSWORD` | SMTP password | Yes |

### JWT Configuration

- **Access Token Lifetime**: 30 minutes
- **Refresh Token Lifetime**: 30 days
- **Token Rotation**: Enabled
- **Algorithm**: HS256

## ?? Authentication

The API uses JWT (JSON Web Tokens) for authentication. Most endpoints require authentication except for registration and public event viewing.

### Authentication Flow

1. **Register** a new user account
2. **Login** to receive access and refresh tokens
3. **Include** the access token in the `Authorization` header for protected endpoints
4. **Refresh** the access token when it expires using the refresh token

### Headers Format

```
Authorization: Bearer <access_token>
```

### Token Endpoints

- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login and receive tokens
- `POST /api/auth/refresh/` - Refresh access token
- `POST /api/auth/logout/` - Logout and blacklist refresh token

## ?? API Endpoints

### Base URL

```
http://localhost:8000/api/
```

### Authentication Endpoints

#### Register User

```http
POST /api/auth/register/
```

**Request Body:**
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "securepassword123",
  "phone_number": "+1234567890",
  "image": "<file>"
}
```

**Response:** `201 Created`
```json
{
  "id": "uuid",
  "username": "johndoe",
  "email": "john@example.com",
  "balance": 1000000,
  "phone_number": "+1234567890",
  "image_url": "https://res.cloudinary.com/...",
  "role": "customer"
}
```

#### Login

```http
POST /api/auth/login/
```

**Request Body:**
```json
{
  "username": "johndoe",
  "password": "securepassword123"
}
```

**Response:** `200 OK`
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### Refresh Token

```http
POST /api/auth/refresh/
```

**Request Body:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response:** `200 OK`
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### Logout

```http
POST /api/auth/logout/
```

**Headers:** `Authorization: Bearer <access_token>`

**Request Body:**
```json
{
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response:** `205 Reset Content`
```json
{
  "message": "success"
}
```

### Customer Endpoints

#### List Events

```http
GET /api/event/
```

**Query Parameters:**
- `category` (optional): Filter by category (`seminar`, `konser`, `horror`, `komedi`, `olahraga`)

**Headers:** `Authorization: Bearer <access_token>` (Customer or Admin)

**Response:** `200 OK`
```json
[
  {
    "id": "uuid",
    "title": "Summer Music Festival",
    "image_url": "https://res.cloudinary.com/...",
    "start_date": "2024-06-01",
    "end_date": "2024-06-03",
    "start_time": "18:00:00",
    "end_time": "23:00:00",
    "city": "Jakarta",
    "price": 150000,
    "category": "konser",
    "organizer": "eventorg1",
    "url_detail": "http://localhost:8000/api/event/uuid/",
    "is_online": false
  }
]
```

#### Get Event Details

```http
GET /api/event/<uuid:id>/
```

**Response:** `200 OK`
```json
{
  "title": "Summer Music Festival",
  "image_url": "https://res.cloudinary.com/...",
  "description": "Annual summer music festival...",
  "start_date": "2024-06-01",
  "end_date": "2024-06-03",
  "start_time": "18:00:00",
  "end_time": "23:00:00",
  "place_name": "Gelora Bung Karno",
  "city": "Jakarta",
  "full_address": "Jl. Pintu Satu Senayan...",
  "location": "Jakarta, Indonesia",
  "category": "konser",
  "organizer": "eventorg1",
  "ticket_type": [
    {
      "id": "uuid",
      "title": "VIP Ticket",
      "start_date": "2024-06-01",
      "end_date": "2024-06-03",
      "start_time": "18:00:00",
      "end_time": "23:00:00",
      "ticket_quantity": 100,
      "ticket_type": "paid",
      "description": "VIP access with backstage pass",
      "price": "250000.00"
    }
  ]
}
```

#### Get Upcoming Events

```http
GET /api/event/upcoming/
```

**Headers:** `Authorization: Bearer <access_token>` (Customer or Admin)

**Response:** `200 OK`
```json
[
  {
    "id": "uuid",
    "title": "Summer Music Festival",
    "image_url": "https://res.cloudinary.com/...",
    ...
  }
]
```

Returns events where the user has purchased tickets.

#### Purchase Ticket

```http
POST /api/ticket/purchase/
```

**Headers:** `Authorization: Bearer <access_token>`

**Request Body:**
```json
{
  "ticket_id": "uuid",
  "price": 150000
}
```

**Note:** `price` is required only for `relawan` ticket type. For other types, use the ticket's default price.

**Response:** `201 Created`
```json
{
  "id": "uuid",
  "owner": "johndoe",
  "title": "VIP Ticket",
  "event": "Summer Music Festival",
  "start_date": "2024-06-01",
  "end_date": "2024-06-03",
  "start_time": "18:00:00",
  "end_time": "23:00:00",
  "ticket_type": "paid",
  "price": "250000.00"
}
```

**Error Responses:**
- `400`: Ticket not found, Ticket sold out, Insufficient balance
- `401`: Unauthorized

### Account Management

#### Get/Update Account

```http
GET /api/account/
PUT /api/account/
PATCH /api/account/
```

**Headers:** `Authorization: Bearer <access_token>`

**Request Body (PUT/PATCH):**
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "phone_number": "+1234567890",
  "password": "newpassword123",
  "image": "<file>"
}
```

**Response:** `200 OK`
```json
{
  "id": "uuid",
  "username": "johndoe",
  "email": "john@example.com",
  "phone_number": "+1234567890",
  "image_url": "https://res.cloudinary.com/...",
  "role": "customer"
}
```

#### Get/Update Account by ID (Admin Only)

```http
GET /api/account/<uuid:id>/
PUT /api/account/<uuid:id>/
PATCH /api/account/<uuid:id>/
```

**Headers:** `Authorization: Bearer <access_token>` (Admin only)

### Event Organizer Endpoints

#### Create Event

```http
POST /api/event-organizer/event/create/
```

**Headers:** `Authorization: Bearer <access_token>` (Event Organizer or Admin)

**Request Body (multipart/form-data):**
```json
{
  "title": "Summer Music Festival",
  "image": "<file>",
  "description": "Annual summer music festival...",
  "start_date": "2024-06-01",
  "end_date": "2024-06-03",
  "start_time": "18:00:00",
  "end_time": "23:00:00",
  "place_name": "Gelora Bung Karno",
  "city": "Jakarta",
  "full_address": "Jl. Pintu Satu Senayan...",
  "location": "Jakarta, Indonesia",
  "category": "konser",
  "is_online": false
}
```

**Category Options:** `seminar`, `konser`, `horror`, `komedi`, `olahraga`

**Response:** `201 Created`
```json
{
  "id": "uuid",
  "title": "Summer Music Festival",
  "image_url": "https://res.cloudinary.com/...",
  "description": "Annual summer music festival...",
  "start_date": "2024-06-01",
  "end_date": "2024-06-03",
  "start_time": "18:00:00",
  "end_time": "23:00:00",
  "place_name": "Gelora Bung Karno",
  "city": "Jakarta",
  "full_address": "Jl. Pintu Satu Senayan...",
  "location": "Jakarta, Indonesia",
  "category": "konser",
  "status": "pending",
  "message": "",
  "owner": "eventorg1",
  "registered_users_url": "http://localhost:8000/api/event-users/uuid/"
}
```

#### Update Event

```http
PUT /api/event-organizer/event/update/<uuid:id>/
PATCH /api/event-organizer/event/update/<uuid:id>/
```

**Headers:** `Authorization: Bearer <access_token>` (Owner or Admin)

**Request Body:** Same as create event

**Response:** `200 OK`

#### List Own Events

```http
GET /api/event-organizer/ownevent/
```

**Headers:** `Authorization: Bearer <access_token>`

**Response:** `200 OK`
```json
[
  {
    "id": "uuid",
    "title": "Summer Music Festival",
    ...
  }
]
```

#### Get Sales Data

```http
GET /api/event-organizer/sales-data/
```

**Headers:** `Authorization: Bearer <access_token>` (Event Organizer or Admin)

**Response:** `200 OK`
```json
{
  "total_sales": 5000000.00,
  "total_active_event": 5,
  "total_sold_ticket": 150,
  "event_data": [
    {
      "title": "Summer Music Festival",
      "status": false,
      "total_sales": 2500000.00,
      "total_sold": 100
    }
  ]
}
```

#### Get Event Users

```http
GET /api/event-users/<uuid:id>/
```

**Headers:** `Authorization: Bearer <access_token>` (Event Organizer or Admin)

**Response:** `200 OK`
```json
[
  {
    "id": "uuid",
    "customer_username": "johndoe",
    "costumer_email": "john@example.com",
    "ticket_type": "paid",
    "price": "250000.00",
    "event": "Summer Music Festival",
    "created_at": "2024-05-15T10:30:00Z"
  }
]
```

#### Create Ticket

```http
POST /api/ticket/create/
```

**Headers:** `Authorization: Bearer <access_token>` (Event Organizer or Admin)

**Request Body:**
```json
{
  "event_id": "uuid",
  "title": "VIP Ticket",
  "start_date": "2024-06-01",
  "end_date": "2024-06-03",
  "start_time": "18:00:00",
  "end_time": "23:00:00",
  "ticket_quantity": 100,
  "ticket_type": "paid",
  "description": "VIP access with backstage pass",
  "price": 250000
}
```

**Ticket Types:**
- `free`: Free ticket (price must be 0)
- `relawan`: Volunteer ticket (price can be set by purchaser)
- `paid`: Paid ticket (price required)

**Response:** `201 Created`
```json
{
  "id": "uuid",
  "title": "VIP Ticket",
  "event_id": "uuid",
  "start_date": "2024-06-01",
  "end_date": "2024-06-03",
  "start_time": "18:00:00",
  "end_time": "23:00:00",
  "ticket_quantity": 100,
  "ticket_type": "paid",
  "description": "VIP access with backstage pass",
  "price": "250000.00"
}
```

**Error Responses:**
- `400`: Price validation errors, Event not found, Not event owner

### Event Organizer Proposals

#### Create Event Organizer Proposal

```http
POST /api/event-organizer-proposal/create/
```

**Headers:** `Authorization: Bearer <access_token>`

**Request Body (multipart/form-data):**
```json
{
  "name": "My Event Organizer Company",
  "category": "Entertainment",
  "description": "We organize various entertainment events...",
  "location": "Jakarta, Indonesia",
  "banner": "<file>",
  "proposal": "<file>"
}
```

**Response:** `201 Created`
```json
{
  "id": "uuid",
  "name": "My Event Organizer Company",
  "category": "Entertainment",
  "description": "We organize various entertainment events...",
  "location": "Jakarta, Indonesia",
  "status": "pending",
  "message": "",
  "owner": "johndoe",
  "url_detail": "http://localhost:8000/api/event-organizer-proposal/uuid/",
  "banner_url": "https://res.cloudinary.com/...",
  "proposal_url": "https://res.cloudinary.com/..."
}
```

#### List Event Organizer Proposals

```http
GET /api/event-organizer-proposal/
```

**Headers:** `Authorization: Bearer <access_token>` (Event Organizer or Admin)

**Response:** `200 OK`
```json
[
  {
    "id": "uuid",
    "name": "My Event Organizer Company",
    ...
  }
]
```

#### Get Event Organizer Proposal Detail

```http
GET /api/event-organizer-proposal/<uuid:id>/
```

**Headers:** `Authorization: Bearer <access_token>` (Owner or Admin)

**Response:** `200 OK`
```json
{
  "id": "uuid",
  "name": "My Event Organizer Company",
  "category": "Entertainment",
  "description": "We organize various entertainment events...",
  "location": "Jakarta, Indonesia",
  "status": "pending",
  "message": "",
  "owner": "johndoe",
  "banner_url": "https://res.cloudinary.com/...",
  "proposal_url": "https://res.cloudinary.com/..."
}
```

### Admin Endpoints

#### List Users

```http
GET /api/admin/user-list/
```

**Headers:** `Authorization: Bearer <access_token>` (Admin only)

**Response:** `200 OK`
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

#### List Event Organizers

```http
GET /api/admin/event-organizers-list/
```

**Headers:** `Authorization: Bearer <access_token>` (Admin only)

**Response:** `200 OK`
```json
[
  {
    "id": "uuid",
    "username": "eventorg1",
    "email": "org@example.com",
    "event_url": "http://localhost:8000/api/admin/event-organizers/uuid/events/"
  }
]
```

#### Get Event Organizer's Events

```http
GET /api/admin/event-organizers/<uuid:id>/events/
```

**Headers:** `Authorization: Bearer <access_token>` (Admin only)

**Response:** `200 OK`
```json
[
  {
    "id": "uuid",
    "title": "Summer Music Festival",
    ...
  }
]
```

#### List Event Proposals

```http
GET /api/admin/event-proposals/
```

**Headers:** `Authorization: Bearer <access_token>` (Admin only)

**Response:** `200 OK`
```json
[
  {
    "id": "uuid",
    "title": "Summer Music Festival",
    "created_at": "2024-05-15T10:30:00Z",
    "event_confirmation_url": "http://localhost:8000/api/admin/event-proposals/uuid/confirm/",
    "event_proposal_detail_url": "http://localhost:8000/api/admin/event-proposals/uuid/"
  }
]
```

#### Get Event Proposal Detail

```http
GET /api/admin/event-proposals/<uuid:id>/
```

**Headers:** `Authorization: Bearer <access_token>` (Admin only)

**Response:** `200 OK`
```json
{
  "id": "uuid",
  "title": "Summer Music Festival",
  ...
}
```

#### Confirm/Reject Event Proposal

```http
PUT /api/admin/event-proposals/<uuid:id>/confirm/
PATCH /api/admin/event-proposals/<uuid:id>/confirm/
```

**Headers:** `Authorization: Bearer <access_token>` (Admin only)

**Request Body:**
```json
{
  "status": "approved",
  "message": "Event approved successfully"
}
```

**Status Options:** `approved`, `rejected`

**Response:** `200 OK`

#### List Event Organizer Proposals

```http
GET /api/admin/event-organizer-proposals/
```

**Headers:** `Authorization: Bearer <access_token>` (Admin only)

**Response:** `200 OK`
```json
[
  {
    "id": "uuid",
    "organizer": "uuid",
    "name": "My Event Organizer Company",
    "created_at": "2024-05-15T10:30:00Z",
    "event_organizer_confirmation_url": "http://localhost:8000/api/admin/event-organizer-proposals/uuid/confirm/",
    "event_organizer_proposal_detail_url": "http://localhost:8000/api/admin/event-organizer-proposals/uuid/"
  }
]
```

#### Get Event Organizer Proposal Detail

```http
GET /api/admin/event-organizer-proposals/<uuid:id>/
```

**Headers:** `Authorization: Bearer <access_token>` (Admin only)

**Response:** `200 OK`

#### Confirm/Reject Event Organizer Proposal

```http
PUT /api/admin/event-organizer-proposals/<uuid:id>/confirm/
PATCH /api/admin/event-organizer-proposals/<uuid:id>/confirm/
```

**Headers:** `Authorization: Bearer <access_token>` (Admin only)

**Request Body:**
```json
{
  "status": "approved",
  "message": "Proposal approved. You are now an event organizer."
}
```

**Note:** When approved, the user's role is automatically updated to `event_organizer`.

**Response:** `200 OK`

## ?? Request/Response Examples

### Example: Complete Ticket Purchase Flow

```bash
# 1. Register
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "securepassword123"
  }'

# 2. Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "password": "securepassword123"
  }'

# 3. List Events
curl -X GET http://localhost:8000/api/event/ \
  -H "Authorization: Bearer <access_token>"

# 4. Purchase Ticket
curl -X POST http://localhost:8000/api/ticket/purchase/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "ticket_id": "uuid"
  }'
```

## ?? Error Handling

The API follows standard HTTP status codes:

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

### Error Response Format

```json
{
  "field_name": ["Error message"],
  "non_field_errors": ["General error message"]
}
```

### Common Error Scenarios

**Insufficient Balance:**
```json
{
  "non_field_errors": ["Insufficient balance"]
}
```

**Ticket Sold Out:**
```json
{
  "non_field_errors": ["Ticket is sold out"]
}
```

**Permission Denied:**
```json
{
  "detail": "Insufficient role permissions."
}
```

**Validation Error:**
```json
{
  "price": ["Price must be greater or equal than 0"]
}
```

## ?? Data Models

### User Model

| Field | Type | Description |
|-------|------|-------------|
| `id` | UUID | Primary key |
| `username` | String | Unique username |
| `email` | String | Unique email |
| `password` | String | Hashed password |
| `balance` | Integer | Account balance (default: 1,000,000) |
| `phone_number` | String | Phone number (optional) |
| `image` | CloudinaryField | Profile image |
| `role` | String | User role: `customer`, `event_organizer`, `administrator` |
| `created_at` | DateTime | Account creation timestamp |

### Event Model

| Field | Type | Description |
|-------|------|-------------|
| `id` | UUID | Primary key |
| `title` | String | Event title |
| `image` | CloudinaryField | Event image |
| `description` | Text | Event description |
| `start_date` | Date | Event start date |
| `end_date` | Date | Event end date |
| `start_time` | Time | Event start time |
| `end_time` | Time | Event end time |
| `place_name` | String | Venue name |
| `city` | String | City name |
| `full_address` | Text | Complete address |
| `location` | Text | Location description |
| `category` | String | Event category |
| `status` | String | `pending`, `approved`, `rejected` |
| `message` | Text | Admin message |
| `is_online` | Boolean | Online event flag |
| `total_sold` | Integer | Total tickets sold |
| `total_sales` | Decimal | Total sales amount |
| `organizer` | ForeignKey | Event organizer (User) |
| `created_at` | DateTime | Creation timestamp |

### Ticket Model

| Field | Type | Description |
|-------|------|-------------|
| `id` | UUID | Primary key |
| `title` | String | Ticket title |
| `event` | ForeignKey | Associated event |
| `start_date` | Date | Ticket validity start |
| `end_date` | Date | Ticket validity end |
| `start_time` | Time | Ticket validity start time |
| `end_time` | Time | Ticket validity end time |
| `ticket_quantity` | Integer | Available quantity |
| `ticket_type` | String | `free`, `relawan`, `paid` |
| `description` | Text | Ticket description |
| `price` | Decimal | Ticket price |
| `created_at` | DateTime | Creation timestamp |

### UserTicket Model

| Field | Type | Description |
|-------|------|-------------|
| `id` | UUID | Primary key |
| `customer` | ForeignKey | Purchasing user |
| `ticket` | ForeignKey | Purchased ticket |
| `price` | Decimal | Purchase price |
| `event` | ForeignKey | Associated event |
| `sales_data` | ForeignKey | Related sales data |
| `created_at` | DateTime | Purchase timestamp |

## ?? Testing

### Running Tests

```bash
cd backend
python manage.py test
```

### Manual Testing with cURL

See [Request/Response Examples](#requestresponse-examples) section for cURL examples.

### Testing with Swagger UI

The API provides interactive Swagger documentation:

```
http://localhost:8000/apidocs/
```

### Testing with Postman

1. Import the OpenAPI schema from `http://localhost:8000/api/schema/`
2. Set up environment variables for the base URL
3. Use the authentication flow to get tokens
4. Test endpoints with the token in the Authorization header

## ?? Deployment

### Production Settings

1. Set `DEBUG=False` in environment variables
2. Configure proper `ALLOWED_HOSTS`
3. Set up secure `SECRET_KEY`
4. Configure PostgreSQL database
5. Set up email backend
6. Configure Cloudinary credentials

### Running with Gunicorn

```bash
cd backend
gunicorn backend.wsgi:application --bind 0.0.0.0:8000
```

### Running with Uvicorn (ASGI)

```bash
cd backend
gunicorn backend.asgi:application -k uvicorn.workers.UvicornWorker
```

### Environment Checklist

- [ ] Set `DEBUG=False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set secure `SECRET_KEY`
- [ ] Configure production database
- [ ] Set up email credentials
- [ ] Configure Cloudinary
- [ ] Set up SSL/HTTPS
- [ ] Configure CORS properly
- [ ] Set up logging
- [ ] Configure static files serving

## ?? Security Best Practices

1. **Always use HTTPS in production**
2. **Keep SECRET_KEY secure and never commit it**
3. **Use strong passwords**
4. **Implement rate limiting** (consider adding django-ratelimit)
5. **Validate all input data**
6. **Use environment variables for sensitive data**
7. **Regularly update dependencies**
8. **Monitor for security vulnerabilities**

## ?? Additional Resources

- [Django REST Framework Documentation](https://www.django-rest-framework.org/)
- [JWT Authentication Guide](https://jwt.io/)
- [Django Documentation](https://docs.djangoproject.com/)
- [OpenAPI Specification](https://swagger.io/specification/)

## ?? Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Code Style

- Follow PEP 8 for Python code
- Use Black for code formatting
- Write docstrings for functions and classes
- Add comments for complex logic

## ?? License

This project is licensed under the MIT License - see the LICENSE file for details.

## ?? Support

For support, please open an issue in the repository or contact the development team.

---

**API Version:** 1.0.0  
**Last Updated:** 2024  
**Maintained by:** Setiket Development Team
