
# MedConnect Backend with FastAPI, PostgreSQL, Docker, Redis, and AI Integration

## Overview

MedConnect is a medical platform designed to connect patients, doctors, and administrators in a unified space for managing healthcare needs. Patients can consult with doctors, share medical data, and access personalized treatment insights. Doctors can track patient histories, document diagnoses, and suggest treatments. With AI integration, MedConnect offers predictive insights on possible drug reactions, ailments, and treatment recommendations based on patient history.

## Table of Contents

1. [Getting Started](#getting-started)
   - [Prerequisites](#prerequisites)
   - [Installation](#installation)
   - [Running the Application](#running-the-application)
2. [Project Structure](#project-structure)
3. [Endpoints](#endpoints)
   - [Authentication](#authentication)
   - [User Roles](#user-roles)
   - [Patient Management](#patient-management)
   - [Doctor Management](#doctor-management)
   - [Medical Data](#medical-data)
   - [Predictive Analysis](#predictive-analysis)
4. [Database Models](#database-models)
5. [Dockerization](#dockerization)
6. [Caching with Redis](#caching-with-redis)
7. [AI Integration](#ai-integration)
8. [Testing](#testing)
9. [Deployment](#deployment)
10. [Contributing](#contributing)
11. [License](#license)

## 1. Getting Started

### Prerequisites

- [Python 3.8+](https://www.python.org/downloads/)
- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [PostgreSQL](https://www.postgresql.org/)
- [Redis](https://redis.io/)
- [AI Model Requirements] (see AI model documentation for setup)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/medconnect.git
   cd medconnect-backend
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

The application will be accessible at `http://localhost:8000`.

## 2. Project Structure

```
medconnect-backend/
|-- app/
|   |-- api/
|   |   |-- __init__.py
|   |   |-- patient.py
|   |   |-- doctor.py
|   |   |-- medical_data.py
|   |   |-- predictive_analysis.py
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
|   |-- ai/
|   |   |-- __init__.py
|   |   |-- predictive_model.py
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

- **POST /login**: Endpoint for user login. Returns an access token.

### User Roles

- **Admin**: Can manage doctors, patients, and access system logs.
- **Doctor**: Can manage patient records, add medical notes, and generate predictions.
- **Patient**: Can view their medical history, consult doctors, and review predicted insights.

### Patient Management

- **POST /patients**: Register a new patient.
- **GET /patients/{patient_id}**: Retrieve patient details by patient ID.

### Doctor Management

- **POST /doctors**: Register a new doctor.
- **GET /doctors/{doctor_id}**: Retrieve doctor details by doctor ID.

### Medical Data

- **POST /medical_data**: Add new medical data entry for a patient.
- **GET /medical_data/{patient_id}**: Retrieve all medical data for a patient.

### Predictive Analysis

- **POST /predict**: Generate predictions based on patient data.
- **GET /predictions/{patient_id}**: Retrieve past predictions for a specific patient.

## 4. Database Models

The backend uses SQLAlchemy ORM to define the following database models:

- **User**: Represents a registered user on the platform.
- **Doctor**: Represents a doctor with medical credentials.
- **Patient**: Represents a patient and their medical history.
- **MedicalData**: Holds patient records and diagnoses.
- **Prediction**: Stores prediction data for future insights.

## 5. Dockerization

The application uses Docker for easy deployment. The Dockerfile and Docker Compose configuration manage FastAPI, PostgreSQL, and Redis.

## 6. Caching with Redis

Redis is used to cache frequently accessed data, such as medical records and predictions, to improve response time and reduce load.

## 7. AI Integration

AI models for prediction are loaded in the `ai/predictive_model.py` module. The models are trained to predict drug interactions, potential health risks, and best treatment options based on historical data.

## 8. Testing

Run unit tests using:

   ```bash
   pytest
   ```

## 9. Deployment

For production deployment:

1. Set environment variables in the `.env` file.
2. Build the Docker image:

   ```bash
   docker build -t medconnect-backend .
   ```

3. Run the container:

   ```bash
   docker run -d -p 8000:8000 --name medconnect-backend-container medconnect-backend
   ```

## 10. Contributing

We welcome contributions to improve MedConnect. Please follow the guidelines in [CONTRIBUTING.md](CONTRIBUTING.md).

## 11. License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
