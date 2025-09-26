# Blog API

A simple Blog Application API built with Django REST Framework, featuring JWT authentication, blog posts, comments, and likes functionality.

## Live Demo

**Live Server:** [https://blog-interview.sydeestack.com/](https://blog-interview.sydeestack.com/)

**API Documentation:** [https://blog-interview.sydeestack.com/api/docs/](https://blog-interview.sydeestack.com/api/docs/)

The default page displays the Swagger documentation interface.

## Tech Stack

- **Backend:** Django 5.2.6, Django REST Framework 3.16.1
- **Database:** MySQL
- **Authentication:** JWT (djangorestframework-simplejwt)
- **API Documentation:** drf-spectacular (OpenAPI/Swagger)
- **Image Upload:** Pillow
- **Environment Management:** python-decouple
- **Production Server:** Gunicorn
- **Containerization:** Docker
- **Deployment:** Railway (with Git webhooks)

## Features

### Authentication
- User signup and login with email
- JWT token-based authentication
- Password reset with OTP via email
- Email-based user management

### Blog Posts
- Create, read, update, delete blog posts
- Image upload for cover photos
- Like/unlike posts
- View users who liked a post
- Pagination support

### Comments
- Create, update, delete comments on posts
- Like/unlike comments
- View users who liked a comment
- Comment validation and moderation

### API Features
- RESTful API design
- Comprehensive API documentation (Swagger/OpenAPI)
- API versioning support
- CORS configuration
- Input validation and error handling
- Production-ready Docker setup

## Prerequisites

- Python 3.11+
- MySQL database
- Docker (optional)
- SMTP credentials for email functionality

## Quick Start

### Option 1: Local Development

1. **Clone the repository**
   ```bash
   git clone <git_url>
   cd django-rest-blog-api
   ```

2. **Create and activate virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment setup**
   ```bash
   cp .env.example .env
   ```
   
   Fill in the required environment variables in `.env`:
   ```env
   SECRET_KEY=your-secret-key
   DEBUG=True
   DB_NAME=your-database-name
   DB_USER=your-database-user
   DB_PASSWORD=your-database-password
   DB_HOST=localhost
   DB_PORT=3306
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   DEFAULT_FROM_EMAIL=noreply@blogapi.com
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Start development server**
   ```bash
   python manage.py runserver
   ```

   The API will be available at `http://localhost:8000/`

### Option 2: Docker

1. **Ensure Docker is installed**

2. **Build the Docker image**
   ```bash
   docker build -t blog-api .
   ```

3. **Create environment file**
   ```bash
   cp .env.example .env
   ```
   
   Fill in your database and SMTP credentials in `.env`

4. **Run the container**
   ```bash
   docker run -d -p 8000:80 --env-file .env blog-api
   ```

5. **Access the application**
   - API: `http://localhost:8000/`
   - Swagger Docs: `http://localhost:8000/api/docs/`

## API Documentation

### Authentication Endpoints
- `POST /api/v1/auth/signup/` - User registration
- `POST /api/v1/auth/login/` - User login
- `POST /api/v1/auth/token/refresh/` - Refresh JWT token
- `POST /api/v1/auth/password-reset/` - Request password reset OTP
- `POST /api/v1/auth/password-confirm/` - Confirm password reset

### Posts Endpoints
- `GET /api/v1/posts/` - List all posts (paginated)
- `POST /api/v1/posts/` - Create a new post
- `GET /api/v1/posts/{id}/` - Get post details
- `PUT /api/v1/posts/{id}/` - Update post
- `DELETE /api/v1/posts/{id}/` - Delete post
- `POST /api/v1/posts/{id}/like/` - Like/unlike post
- `GET /api/v1/posts/{id}/likes/` - Get post likes

### Comments Endpoints
- `GET /api/v1/comments/` - List comments (with post filter)
- `POST /api/v1/comments/` - Create a new comment
- `PUT /api/v1/comments/{id}/` - Update comment
- `DELETE /api/v1/comments/{id}/` - Delete comment
- `POST /api/v1/comments/{id}/like/` - Like/unlike comment
- `GET /api/v1/comments/{id}/likes/` - Get comment likes

## Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `SECRET_KEY` | Django secret key | Yes | - |
| `DEBUG` | Debug mode | No | True |
| `DB_NAME` | MySQL database name | Yes | - |
| `DB_USER` | MySQL username | Yes | - |
| `DB_PASSWORD` | MySQL password | Yes | - |
| `DB_HOST` | MySQL host | No | localhost |
| `DB_PORT` | MySQL port | No | 3306 |
| `EMAIL_HOST` | SMTP host | No | smtp.gmail.com |
| `EMAIL_PORT` | SMTP port | No | 587 |
| `EMAIL_HOST_USER` | SMTP username | Yes | - |
| `EMAIL_HOST_PASSWORD` | SMTP password | Yes | - |
| `DEFAULT_FROM_EMAIL` | From email address | No | noreply@blogapi.com |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts | No | localhost,127.0.0.1 |
| `API_VERSION` | API version | No | v1 |
| `OTP_EXPIRY_MINUTES` | OTP expiry time | No | 10 |

## Project Structure

```
django-rest-blog-api/
├── authentication/          # User authentication app
│   ├── models.py           # Custom User model, PasswordResetOTP
│   ├── serializers.py      # Auth serializers
│   ├── views.py            # Auth API views
│   ├── urls.py             # Auth URL patterns
│   ├── backends.py         # Email authentication backend
│   └── utils.py            # Email utilities
├── posts/                  # Blog posts app
│   ├── models.py           # Post model
│   ├── serializers.py      # Post serializers
│   ├── views.py            # Post API views
│   └── urls.py             # Post URL patterns
├── comments/               # Comments app
│   ├── models.py           # Comment model
│   ├── serializers.py      # Comment serializers
│   ├── views.py            # Comment API views
│   └── urls.py             # Comment URL patterns
├── blog/                   # Main project
│   ├── settings.py         # Django settings
│   ├── urls.py             # Main URL configuration
│   └── wsgi.py             # WSGI configuration
├── media/                  # Uploaded files
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose setup
├── start.sh               # Production startup script
└── .env.example           # Environment variables template
```

## Deployment

The application is deployed on Railway with automatic deployment via Git webhooks:

1. **Push to main branch** triggers automatic deployment
2. **Environment variables** are configured in Railway dashboard
3. **Database** is hosted on Railway MySQL
4. **Static files** are served by Gunicorn
5. **Health checks** monitor application status

## Testing

The API includes comprehensive validation and error handling:

- Input validation on all endpoints
- Proper HTTP status codes
- Detailed error messages
- JWT token validation
- Permission-based access control

## API Features

- **JWT Authentication:** Secure token-based authentication
- **Email-based Login:** Users login with email instead of username
- **Password Reset:** OTP-based password reset via email
- **Image Upload:** Support for post cover photos
- **Like System:** Like/unlike posts and comments
- **Pagination:** Efficient data loading with pagination
- **API Documentation:** Interactive Swagger/OpenAPI documentation
- **CORS Support:** Cross-origin resource sharing configuration
- **Production Ready:** Docker containerization with Gunicorn

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is part of a technical interview assessment.

---

**Live Demo:** [https://blog-interview.sydeestack.com/](https://blog-interview.sydeestack.com/)  
**API Documentation:** [https://blog-interview.sydeestack.com/api/docs/](https://blog-interview.sydeestack.com/api/docs/)
