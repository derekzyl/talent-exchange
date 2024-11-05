# Flow Backend with FastAPI, PostgreSQL, Docker, and Redis

## Overview

Flow is a platform that connects artisans with both soft skills and manual skills to individuals who are looking for their services. This backend application is built using FastAPI, PostgreSQL as the database, Docker for containerization, and Redis for caching purposes.

## Table of Contents

1. [Getting Started](#getting-started)
   - [Prerequisites](#prerequisites)
   - [Installation](#installation)
   - [Running the Application](#running-the-application)
2. [Project Structure](#project-structure)
3. [Endpoints](#endpoints)
   - [Authentication](#authentication)
   - [User](#user)
   - [Artisan](#artisan)
   - [Service](#service)
   - [Booking](#booking)
   - [Search](#search)
4. [Database Models](#database-models)
5. [Dockerization](#dockerization)
6. [Caching with Redis](#caching-with-redis)
7. [Testing](#testing)
8. [Deployment](#deployment)
9. [Contributing](#contributing)
10. [License](#license)

## 1. Getting Started

### Prerequisites

- [Python 3.8+](https://www.python.org/downloads/)
- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [PostgreSQL](https://www.postgresql.org/)
- [Redis](https://redis.io/)

### Installation

1. Clone the repository:

```bash
git clone https://github.com/derekzyl/flow.git
cd flow/flow-backend
```

2. Create a virtual environment and activate it:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

### Running the Application

1. Start PostgreSQL and Redis services using Docker Compose:

```bash
docker-compose up -d
```

2. Initialize the database and create tables:

```bash
python app/db/init_db.py
```

3. Run the FastAPI application:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The application is now running and accessible at `http://localhost:8000`.

## 2. Project Structure

```
flow-backend/
|-- app/
|   |-- api/
|   |   |-- __init__.py
|   |   |-- artisan.py
|   |   |-- booking.py
|   |   |-- search.py
|   |   |-- service.py
|   |   |-- user.py
|   |-- db/
|   |   |-- __init__.py
|   |   |-- base.py
|   |   |-- init_db.py
|   |   |-- models.py
|   |   |-- schemas.py
|   |-- core/
|   |   |-- __init__.py
|   |   |-- config.py
|   |   |-- security.py
|   |-- main.py
|-- tests/
|   |-- __init__.py
|   |-- test_endpoints.py
|-- .env
|-- .gitignore
|-- docker-compose.yml
|-- Dockerfile
|-- README.md
|-- requirements.txt
```

## 3. Endpoints

### Authentication

- **POST /login**: Endpoint for user login. It returns an access token.

### User

- **POST /users**: Endpoint for user registration.
- **GET /users/{user_id}**: Get user details by user ID.

### Artisan

- **POST /artisans**: Endpoint for artisan registration.
- **GET /artisans/{artisan_id}**: Get artisan details by artisan ID.

### Service

- **POST /services**: Endpoint for creating a new service.
- **GET /services/{service_id}**: Get service details by service ID.

### Booking

- **POST /bookings**: Endpoint for creating a booking.
- **GET /bookings/{booking_id}**: Get booking details by booking ID.

### Search

- **GET /search**: Endpoint for searching artisans and services based on specific criteria.

## 4. Database Models

The backend uses SQLAlchemy ORM to define the following database models:

- User: Represents a registered user on the platform.
- Artisan: Represents an artisan with soft skills or manual skills.
- Service: Represents a service provided by an artisan.
- Booking: Represents a booking made by a user for a specific service.

## 5. Dockerization

The application can be easily deployed using Docker. The Dockerfile defines the environment and dependencies needed to run the application. Docker Compose is used to manage the PostgreSQL and Redis services required by the application.

## 6. Caching with Redis

Redis is used for caching purposes to improve the performance of frequently accessed data, such as search results and service details.

## 7. Testing

Unit tests are included in the `tests` directory. You can run the tests using the following command:

```bash
pytest
```

## 8. Deployment

To deploy the application in production, follow these steps:

1. Set the appropriate environment variables in the `.env` file, such as database credentials and secret keys.

2. Build the Docker image:

```bash
docker build -t flow-backend .
```

3. Run the Docker container:

```bash
docker run -d -p 8000:8000 --name flow-backend-container flow-backend
```

## 9. Contributing

We welcome contributions to improve the Flow backend. To contribute, please follow the guidelines outlined in [CONTRIBUTING.md](CONTRIBUTING.md).

## 10. License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for more details.
# servital-backend
# backend
