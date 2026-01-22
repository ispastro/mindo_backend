# Mindo Backend API Documentation

**Version:** 1.0.0  
**Base URL:** `https://your-app-name.onrender.com`  
**Protocol:** HTTPS  
**Authentication:** JWT Bearer Token

---

## Table of Contents

1. [Overview](#overview)
2. [Authentication Flow](#authentication-flow)
3. [API Endpoints](#api-endpoints)
4. [Error Handling](#error-handling)
5. [Code Examples](#code-examples)
6. [Rate Limits](#rate-limits)

---

## Overview

The Mindo Backend API is a RESTful API for managing user authentication and item tracking. All responses are in JSON format.

### Base URL
```
Production: https://your-app-name.onrender.com
Development: http://localhost:8000
```

### Content Type
All requests and responses use `application/json`

### Authentication
Protected endpoints require a JWT token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

---

## Authentication Flow

### 1. User Registration
### 2. User Login (Get JWT Token)
### 3. Use Token for Protected Endpoints

---

## API Endpoints

### 🔓 Public Endpoints

#### 1. Welcome Message
```http
GET /
```

**Response:**
```json
{
  "message": "Welcome to Mindo Backend API"
}
```

---

#### 2. Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy"
}
```

---

#### 3. Ping (Keep Alive)
```http
GET /ping
```

**Response:**
```json
{
  "status": "alive",
  "timestamp": "2026-01-20T20:30:00.123456",
  "service": "Mindo Backend API",
  "environment": "production"
}
```

---

### 🔐 Authentication Endpoints

#### 1. User Signup
```http
POST /api/auth/signup
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123",
  "name": "John Doe"
}
```

**Validation Rules:**
- `email`: Valid email format, max 255 characters (required)
- `password`: Min 8 characters, max 100 characters (required)
- `name`: Max 255 characters (optional)

**Success Response (201 Created):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "name": "John Doe",
  "created_at": "2026-01-20T20:30:00.123456"
}
```

**Error Response (409 Conflict):**
```json
{
  "detail": "Email already registered"
}
```

**Error Response (422 Validation Error):**
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
    }
  ]
}
```

---

#### 2. User Login
```http
POST /api/auth/login
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123"
}
```

**Success Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "name": "John Doe",
    "created_at": "2026-01-20T20:30:00.123456"
  }
}
```

**Error Response (401 Unauthorized):**
```json
{
  "detail": "Invalid email or password"
}
```

**Token Expiry:** 7 days (10,080 minutes)

---

#### 3. Get Current User
```http
GET /api/auth/me
```

**Headers:**
```
Authorization: Bearer <your_jwt_token>
```

**Success Response (200 OK):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "name": "John Doe",
  "created_at": "2026-01-20T20:30:00.123456"
}
```

**Error Response (401 Unauthorized):**
```json
{
  "detail": "Invalid or expired token"
}
```

---

### 📦 Items Endpoints (All Protected)

#### 1. Create Item
```http
POST /api/items
```

**Headers:**
```
Authorization: Bearer <your_jwt_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "name": "Car Keys",
  "location": "Kitchen counter, next to the coffee maker"
}
```

**Validation Rules:**
- `name`: Required, min 1 char, max 255 characters
- `location`: Required, min 1 char, max 1000 characters

**Success Response (201 Created):**
```json
{
  "id": "660e8400-e29b-41d4-a716-446655440001",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Car Keys",
  "location": "Kitchen counter, next to the coffee maker",
  "created_at": "2026-01-20T20:30:00.123456",
  "updated_at": "2026-01-20T20:30:00.123456"
}
```

---

#### 2. List Items (with Pagination & Search)
```http
GET /api/items?page=1&page_size=10&query=keys
```

**Headers:**
```
Authorization: Bearer <your_jwt_token>
```

**Query Parameters:**
- `page` (optional): Page number, default 1, min 1
- `page_size` (optional): Items per page, default 10, min 1, max 100
- `query` (optional): Search term (searches in name and location)

**Success Response (200 OK):**
```json
{
  "data": [
    {
      "id": "660e8400-e29b-41d4-a716-446655440001",
      "user_id": "550e8400-e29b-41d4-a716-446655440000",
      "name": "Car Keys",
      "location": "Kitchen counter, next to the coffee maker",
      "created_at": "2026-01-20T20:30:00.123456",
      "updated_at": "2026-01-20T20:30:00.123456"
    },
    {
      "id": "660e8400-e29b-41d4-a716-446655440002",
      "user_id": "550e8400-e29b-41d4-a716-446655440000",
      "name": "House Keys",
      "location": "Bedroom nightstand drawer",
      "created_at": "2026-01-20T20:31:00.123456",
      "updated_at": "2026-01-20T20:31:00.123456"
    }
  ],
  "pagination": {
    "page": 1,
    "page_size": 10,
    "total_items": 2,
    "total_pages": 1,
    "has_next_page": false,
    "has_previous_page": false
  }
}
```

**Error Response (400 Bad Request):**
```json
{
  "detail": "Page must be >= 1"
}
```

---

#### 3. Get Single Item
```http
GET /api/items/{item_id}
```

**Headers:**
```
Authorization: Bearer <your_jwt_token>
```

**Path Parameters:**
- `item_id`: UUID of the item

**Success Response (200 OK):**
```json
{
  "id": "660e8400-e29b-41d4-a716-446655440001",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Car Keys",
  "location": "Kitchen counter, next to the coffee maker",
  "created_at": "2026-01-20T20:30:00.123456",
  "updated_at": "2026-01-20T20:30:00.123456"
}
```

**Error Response (404 Not Found):**
```json
{
  "detail": "Item not found"
}
```

**Error Response (403 Forbidden):**
```json
{
  "detail": "Not authorized to access this item"
}
```

---

#### 4. Update Item
```http
PATCH /api/items/{item_id}
```

**Headers:**
```
Authorization: Bearer <your_jwt_token>
Content-Type: application/json
```

**Path Parameters:**
- `item_id`: UUID of the item

**Request Body (all fields optional):**
```json
{
  "name": "Car Keys - Updated",
  "location": "Living room coffee table"
}
```

**Success Response (200 OK):**
```json
{
  "id": "660e8400-e29b-41d4-a716-446655440001",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Car Keys - Updated",
  "location": "Living room coffee table",
  "created_at": "2026-01-20T20:30:00.123456",
  "updated_at": "2026-01-20T20:35:00.123456"
}
```

**Error Response (404 Not Found):**
```json
{
  "detail": "Item not found"
}
```

**Error Response (403 Forbidden):**
```json
{
  "detail": "Not authorized to update this item"
}
```

---

#### 5. Delete Item
```http
DELETE /api/items/{item_id}
```

**Headers:**
```
Authorization: Bearer <your_jwt_token>
```

**Path Parameters:**
- `item_id`: UUID of the item

**Success Response (204 No Content):**
```
(Empty response body)
```

**Error Response (404 Not Found):**
```json
{
  "detail": "Item not found"
}
```

**Error Response (403 Forbidden):**
```json
{
  "detail": "Not authorized to delete this item"
}
```

---

## Error Handling

### HTTP Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request successful |
| 201 | Created | Resource created successfully |
| 204 | No Content | Request successful, no content to return |
| 400 | Bad Request | Invalid request parameters |
| 401 | Unauthorized | Missing or invalid authentication token |
| 403 | Forbidden | Authenticated but not authorized |
| 404 | Not Found | Resource not found |
| 409 | Conflict | Resource already exists (duplicate) |
| 422 | Unprocessable Entity | Validation error |
| 500 | Internal Server Error | Server error |

### Error Response Format

All errors follow this structure:
```json
{
  "detail": "Error message here"
}
```

For validation errors (422):
```json
{
  "detail": [
    {
      "loc": ["body", "field_name"],
      "msg": "error message",
      "type": "error_type"
    }
  ]
}
```

---

## Code Examples

### JavaScript/TypeScript (Fetch API)

#### 1. User Signup
```javascript
const signup = async (email, password, name) => {
  const response = await fetch('https://your-app.onrender.com/api/auth/signup', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ email, password, name }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail);
  }

  return await response.json();
};
```

#### 2. User Login
```javascript
const login = async (email, password) => {
  const response = await fetch('https://your-app.onrender.com/api/auth/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ email, password }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail);
  }

  const data = await response.json();
  // Store token in localStorage or secure storage
  localStorage.setItem('access_token', data.access_token);
  return data;
};
```

#### 3. Get Current User
```javascript
const getCurrentUser = async () => {
  const token = localStorage.getItem('access_token');
  
  const response = await fetch('https://your-app.onrender.com/api/auth/me', {
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    throw new Error('Unauthorized');
  }

  return await response.json();
};
```

#### 4. Create Item
```javascript
const createItem = async (name, location) => {
  const token = localStorage.getItem('access_token');
  
  const response = await fetch('https://your-app.onrender.com/api/items', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
    },
    body: JSON.stringify({ name, location }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail);
  }

  return await response.json();
};
```

#### 5. List Items with Pagination
```javascript
const listItems = async (page = 1, pageSize = 10, query = '') => {
  const token = localStorage.getItem('access_token');
  const params = new URLSearchParams({ page, page_size: pageSize });
  if (query) params.append('query', query);
  
  const response = await fetch(
    `https://your-app.onrender.com/api/items?${params}`,
    {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    }
  );

  if (!response.ok) {
    throw new Error('Failed to fetch items');
  }

  return await response.json();
};
```

#### 6. Update Item
```javascript
const updateItem = async (itemId, updates) => {
  const token = localStorage.getItem('access_token');
  
  const response = await fetch(
    `https://your-app.onrender.com/api/items/${itemId}`,
    {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify(updates),
    }
  );

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail);
  }

  return await response.json();
};
```

#### 7. Delete Item
```javascript
const deleteItem = async (itemId) => {
  const token = localStorage.getItem('access_token');
  
  const response = await fetch(
    `https://your-app.onrender.com/api/items/${itemId}`,
    {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    }
  );

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail);
  }

  return true; // 204 No Content
};
```

---

### React Example (with Axios)

```javascript
import axios from 'axios';

const API_BASE_URL = 'https://your-app.onrender.com';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Redirect to login
      localStorage.removeItem('access_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// API functions
export const authAPI = {
  signup: (email, password, name) =>
    api.post('/api/auth/signup', { email, password, name }),
  
  login: (email, password) =>
    api.post('/api/auth/login', { email, password }),
  
  getCurrentUser: () =>
    api.get('/api/auth/me'),
};

export const itemsAPI = {
  create: (name, location) =>
    api.post('/api/items', { name, location }),
  
  list: (page = 1, pageSize = 10, query = '') =>
    api.get('/api/items', { params: { page, page_size: pageSize, query } }),
  
  get: (itemId) =>
    api.get(`/api/items/${itemId}`),
  
  update: (itemId, updates) =>
    api.patch(`/api/items/${itemId}`, updates),
  
  delete: (itemId) =>
    api.delete(`/api/items/${itemId}`),
};
```

---

## Rate Limits

Currently, there are no rate limits enforced. However, please be respectful:
- Avoid excessive requests
- Implement proper caching on the frontend
- Use pagination for large datasets

---

## Best Practices

### 1. Token Management
- Store JWT token securely (localStorage or httpOnly cookies)
- Check token expiry before making requests
- Implement token refresh logic
- Clear token on logout

### 2. Error Handling
- Always handle 401 errors (redirect to login)
- Show user-friendly error messages
- Log errors for debugging

### 3. Performance
- Use pagination for lists
- Implement search debouncing
- Cache user data when appropriate
- Use optimistic UI updates

### 4. Security
- Never expose tokens in URLs
- Use HTTPS in production
- Validate user input on frontend
- Implement CSRF protection if using cookies

---

## Support

For issues or questions:
- **API Documentation:** https://your-app.onrender.com/docs
- **GitHub Issues:** [Your repo URL]
- **Email:** your-email@example.com

---

**Last Updated:** January 20, 2026  
**API Version:** 1.0.0
