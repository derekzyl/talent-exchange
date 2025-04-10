# Talent Exchange Platform API

## Overview

The Talent Exchange Platform API is a robust backend service designed to facilitate connections between professionals, employers, and opportunities. Built with FastAPI and modern Python practices, this platform enables efficient talent discovery, skill matching, and professional relationship management.

## Features

- **User Management**: Registration, authentication, profile creation and management
- **Skill Cataloging**: Comprehensive skill tracking, categorization, and verification
- **Search & Matching**: Advanced algorithms to connect talent with opportunities
- **JWT Authentication**: Secure, token-based API access
- **Scalable Architecture**: Built with performance and growth in mind
- **Comprehensive Documentation**: Interactive API docs with testing capabilities
- **Error Handling**: Detailed error responses for better debugging and user experience

## Prerequisites

- Python 3.8+
- PostgreSQL (recommended) or other supported database
- Internet connection for dependency installation

## Installation & Setup

### Quick Start (Recommended)

Execute the automated setup script:

```bash
sh run.sh
```

This script:
1. Checks for and creates an `.env` file if not present
2. Installs necessary system dependencies (pip)
3. Sets up Python environment with pipenv
4. Installs project dependencies
5. Launches the FastAPI server

### Manual Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-organization/talent-exchange.git
   cd talent-exchange
   ```

2. **Set up environment variables**:
   ```bash
   cp example.env .env
   ```
   Edit `.env` with appropriate configuration settings:
   - Database connection details
   - JWT secret key
   - Email service configuration
   - Other environment-specific settings

3. **Install dependencies**:
   ```bash
   pip install pipenv
   pipenv install
   pipenv run pip install -r requirements.txt
   ```

4. **Initialize the database**:
   ```bash
   pipenv run python -m app.scripts.init_db
   ```

5. **Start the server**:
   ```bash
   pipenv run fastapi run
   ```
   For development with hot-reload:
   ```bash
   pipenv run uvicorn app.main:app --reload
   ```

## API Documentation

Once the server is running, access the interactive API documentation:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Authentication

The API uses JWT bearer token authentication:

### Public Endpoints (No Authentication Required)
- `/` - API home/status
- `/api/v1/auth/login` - User login
- `/api/v1/auth/signup` - User registration
- `/auth/register` - Alternative registration endpoint
- `/docs`, `/redoc`, `/openapi.json` - API documentation

### Protected Endpoints
All other endpoints require authentication via JWT bearer token:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

Tokens are obtained through the login endpoint and typically expire after 24 hours.

## API Structure

- `/api/v1/auth/*` - Authentication operations
- `/api/v1/users/*` - User profile management
- `/api/v1/skill/*` - Skill definition and management
- `/api/v1/opportunities/*` - Job/project listings
- `/api/v1/matches/*` - Talent-opportunity matching endpoints

## Development

### Environment Configuration

Critical environment variables include:
- `DATABASE_URL`: Connection string for your database
- `JWT_SECRET_KEY`: Secret key for JWT token generation/validation
- `EMAIL_SERVICE_*`: Email service configuration for notifications

### Running Tests

```bash
pipenv run pytest
```

For coverage report:
```bash
pipenv run pytest --cov=app
```

### Database Migrations

```bash
pipenv run alembic revision --autogenerate -m "description"
pipenv run alembic upgrade head
```

## Deployment

### Production Considerations

1. Use a production-grade ASGI server:
   ```bash
   pipenv run gunicorn app.main:app -k uvicorn.workers.UvicornWorker
   ```

2. Set appropriate environment variables:
   - `ENVIRONMENT=production`
   - Secure database credentials
   - Production-specific service URLs

3. Implement rate limiting and additional security measures

### Docker Support

```bash
docker build -t talent-exchange-api .
docker run -p 8000:8000 --env-file .env talent-exchange-api
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a pull request

## Troubleshooting

### Common Issues

- **Database Connection Problems**: Verify database credentials in `.env`
- **JWT Authentication Failures**: Check token expiration and secret key
- **Missing Dependencies**: Run `pipenv install` to update environment

For more help, check the logs or create an issue in the repository.

## License

[MIT License](LICENSE)