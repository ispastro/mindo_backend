# Mindo API - Quick Reference

## Base URL
```
https://your-app-name.onrender.com
```

## Authentication
```
Authorization: Bearer <token>
```

---

## Endpoints Summary

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/` | No | Welcome message |
| GET | `/health` | No | Health check |
| GET | `/ping` | No | Keep alive |
| POST | `/api/auth/signup` | No | Register user |
| POST | `/api/auth/login` | No | Login user |
| GET | `/api/auth/me` | Yes | Get current user |
| POST | `/api/items` | Yes | Create item |
| GET | `/api/items` | Yes | List items |
| GET | `/api/items/{id}` | Yes | Get item |
| PATCH | `/api/items/{id}` | Yes | Update item |
| DELETE | `/api/items/{id}` | Yes | Delete item |

---

## Quick Start

### 1. Signup
```javascript
POST /api/auth/signup
{
  "email": "user@example.com",
  "password": "SecurePass123",
  "name": "John Doe"
}
```

### 2. Login
```javascript
POST /api/auth/login
{
  "email": "user@example.com",
  "password": "SecurePass123"
}
// Returns: { access_token, token_type, user }
```

### 3. Use Token
```javascript
GET /api/auth/me
Headers: { Authorization: "Bearer <token>" }
```

### 4. Create Item
```javascript
POST /api/items
Headers: { Authorization: "Bearer <token>" }
{
  "name": "Car Keys",
  "location": "Kitchen counter"
}
```

### 5. List Items
```javascript
GET /api/items?page=1&page_size=10&query=keys
Headers: { Authorization: "Bearer <token>" }
```

---

## Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 204 | No Content (Delete) |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 409 | Conflict (Duplicate) |
| 422 | Validation Error |

---

## Common Errors

### 401 Unauthorized
```json
{ "detail": "Invalid or expired token" }
```
**Solution:** Login again to get new token

### 409 Conflict
```json
{ "detail": "Email already registered" }
```
**Solution:** Use different email or login

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address"
    }
  ]
}
```
**Solution:** Fix validation errors

---

## TypeScript Types

```typescript
// User
interface User {
  id: string;
  email: string;
  name: string | null;
  created_at: string;
}

// Item
interface Item {
  id: string;
  user_id: string;
  name: string;
  location: string;
  created_at: string;
  updated_at: string;
}

// Login Response
interface LoginResponse {
  access_token: string;
  token_type: string;
  user: User;
}

// Paginated Response
interface PaginatedItems {
  data: Item[];
  pagination: {
    page: number;
    page_size: number;
    total_items: number;
    total_pages: number;
    has_next_page: boolean;
    has_previous_page: boolean;
  };
}
```

---

## Testing

**Swagger UI:** https://your-app-name.onrender.com/docs

**Test Credentials:**
```
Email: test@example.com
Password: Test1234
```

---

For full documentation, see [API_DOCUMENTATION.md](./API_DOCUMENTATION.md)
