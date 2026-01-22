# Mindo Backend API

A production-ready FastAPI backend for the Mindo voice-first item tracking application.

## 🚀 Features

- ✅ **JWT Authentication** - Secure user authentication with 7-day token expiry
- ✅ **User Management** - Registration, login, and profile endpoints
- ✅ **Items CRUD** - Complete create, read, update, delete operations
- ✅ **Search & Pagination** - Efficient data retrieval with filtering
- ✅ **Row-Level Security** - Users can only access their own data
- ✅ **PostgreSQL Database** - Production-ready with Supabase
- ✅ **Password Hashing** - Bcrypt encryption for security
- ✅ **CORS Support** - Ready for frontend integration

## 📋 API Endpoints

### Authentication
- `POST /api/auth/signup` - Register new user
- `POST /api/auth/login` - Login and get JWT token
- `GET /api/auth/me` - Get current user info (protected)

### Items
- `POST /api/items` - Create new item (protected)
- `GET /api/items` - List items with pagination & search (protected)
- `GET /api/items/{id}` - Get single item (protected)
- `PATCH /api/items/{id}` - Update item (protected)
- `DELETE /api/items/{id}` - Delete item (protected)

### Health
- `GET /` - Welcome message
- `GET /health` - Health check

## 🛠️ Tech Stack

- **Framework:** FastAPI
- **Database:** PostgreSQL (Supabase)
- **ORM:** SQLModel
- **Authentication:** JWT (python-jose)
- **Password Hashing:** Bcrypt
- **Validation:** Pydantic

## 📦 Installation

### Prerequisites
- Python 3.11+
- PostgreSQL database (Supabase account)

### Local Setup

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd mindo_backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # Mac/Linux
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create `.env` file:**
   ```env
   PROJECT_NAME="Mindo Backend API"
   DATABASE_URL="postgresql://user:password@host:5432/database"
   SECRET_KEY="your-secret-key-here"
   ALGORITHM="HS256"
   ACCESS_TOKEN_EXPIRE_MINUTES=10080
   CORS_ORIGINS="http://localhost:3000,http://localhost:5173"
   ENVIRONMENT="development"
   DEBUG=True
   ```

5. **Generate SECRET_KEY:**
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

6. **Run the server:**
   ```bash
   uvicorn app.main:app --reload
   ```

7. **Access API documentation:**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## 🚀 Deployment to Render

### Step 1: Prepare Your Repository
1. Commit all changes to GitHub
2. Make sure `.env` is in `.gitignore`

### Step 2: Deploy on Render

1. **Go to [Render.com](https://render.com)** and sign up with GitHub

2. **Create New Web Service:**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select your `mindo_backend` repo

3. **Configure the service:**
   - **Name:** `mindo-backend` (or your choice)
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

4. **Add Environment Variables:**
   Click "Advanced" → "Add Environment Variable" and add:
   
   ```
   PROJECT_NAME = Mindo Backend API
   DATABASE_URL = your-supabase-connection-string
   SECRET_KEY = your-generated-secret-key
   ALGORITHM = HS256
   ACCESS_TOKEN_EXPIRE_MINUTES = 10080
   CORS_ORIGINS = https://your-frontend-domain.com
   ENVIRONMENT = production
   DEBUG = False
   ```

5. **Deploy:**
   - Click "Create Web Service"
   - Wait 2-3 minutes for deployment
   - Your API will be live at: `https://mindo-backend.onrender.com`

### Step 3: Test Your Deployment

Visit: `https://your-app-name.onrender.com/docs`

You should see the Swagger documentation!

## 🔒 Security Notes

- Never commit `.env` file to git
- Use strong SECRET_KEY (32+ characters)
- Keep DATABASE_URL private
- Use HTTPS in production
- Set DEBUG=False in production

## 📝 Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `PROJECT_NAME` | Application name | `Mindo Backend API` |
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host:5432/db` |
| `SECRET_KEY` | JWT signing key | `generated-secret-key` |
| `ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiry time | `10080` (7 days) |
| `CORS_ORIGINS` | Allowed frontend origins | `http://localhost:3000` |
| `ENVIRONMENT` | Environment mode | `development` or `production` |
| `DEBUG` | Debug mode | `True` or `False` |

## 🧪 Testing

Run tests:
```bash
pytest
```

## 📚 Project Structure

```
mindo_backend/
├── app/
│   ├── dependencies/
│   │   └── auth.py          # Authentication dependency
│   ├── models/
│   │   └── models.py        # Database models
│   ├── routers/
│   │   ├── auth.py          # Authentication endpoints
│   │   └── items.py         # Items CRUD endpoints
│   ├── schemas/
│   │   ├── user.py          # User Pydantic schemas
│   │   └── item.py          # Item Pydantic schemas
│   ├── utils/
│   │   ├── security.py      # Password hashing
│   │   └── jwt.py           # JWT token utilities
│   ├── config.py            # Configuration management
│   ├── database.py          # Database connection
│   └── main.py              # FastAPI application
├── .env                     # Environment variables (not in git)
├── .gitignore              # Git ignore rules
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📄 License

MIT License

## 👨‍💻 Author 

Built with ❤️ for the Mindo voice-first application

## 🔗 Links

- **Live Demo:** https://mindo-mine.vercel.app
- **API Documentation:** https://mindo-backend-1.onrender.com/docs
- **Deployed Backend:** https://mindo-backend-1.onrender.com
- **Frontend Repository:** https://github.com/ispastro/mindo-4g.git

---

**Note:** The free tier on Render sleeps after 15 minutes of inactivity. First request after sleep may take 30-60 seconds to wake up.
