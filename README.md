# Clip Vault API

A RESTful API built with FastAPI, SQLAlchemy, and SQLite for managing video clip metadata.

This project was developed as a take-home assessment for the Software Engineer Intern role at Astraa Innovation.

## Live Demo

- **GitHub Repository:** https://github.com/yourusername/clipvaultapi
- **Live API (Render):** https://clipvaultapi.onrender.com
- **Swagger UI:** https://clipvaultapi.onrender.com/docs
- **OpenAPI Schema:** https://clipvaultapi.onrender.com/openapi.json

---
---

# Features

- Create a new clip
- Retrieve all clips with pagination
- Retrieve a single clip by ID
- Update a clip's processing status
- Delete a clip
- Health check endpoint
- Input validation using Pydantic
- Duplicate filename prevention
- SQLite database persistence
- Unit and integration tests using Pytest

---

# Technology Stack

- Python 3.13
- FastAPI
- SQLAlchemy 2.0
- SQLite
- Pydantic v2
- Pytest
- Uvicorn

---

# Project Structure

```text
clipvaultapi/
│
├── main.py                 # FastAPI application and API endpoints
├── database.py             # Database configuration
├── models.py               # SQLAlchemy models
├── schemas.py              # Pydantic request/response models
├── clips.db                # SQLite database
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_clips.py
│
├── requirements.txt
└── README.md
```

---

# Database

The application uses a single SQLite table.

## clips

| Column | Type | Description |
|---------|------|-------------|
| id | Integer | Primary Key |
| title | String(100) | Clip title |
| filename | String(255) | Unique video filename |
| upload_time | DateTime | Timestamp of upload |
| status | Enum | uploaded, processing, ready |

---

# API Endpoints

## GET /clips

Returns a paginated list of clips.

### Query Parameters

| Parameter | Description |
|------------|-------------|
| limit | Maximum number of clips to return |
| offset | Number of clips to skip |
| status | Optional filter (`uploaded`, `processing`, `ready`) |

### Example

```http
GET /clips?limit=10&offset=0&status=uploaded
```

---

## GET /clips/{clip_id}

Returns a single clip by its ID.

### Example

```http
GET /clips/5
```

---

## POST /clips

Creates a new clip.

### Example Request

```json
{
  "title": "Holiday",
  "filename": "holiday.mp4",
  "status": "uploaded"
}
```

### Example Response

```json
{
  "message": "Clip created successfully.",
  "clip": {
    "id": 1,
    "title": "Holiday",
    "filename": "holiday.mp4",
    "upload_time": "2026-07-04T15:30:21",
    "status": "uploaded"
  }
}
```

---

## PATCH /clips/{clip_id}

Updates the processing status of a clip.

### Example Request

```json
{
  "status": "ready"
}
```

---

## DELETE /clips/{clip_id}

Deletes a clip.

### Response

```http
204 No Content
```

---

## GET /health

Returns the API health status.

### Example Response

```json
{
  "status": "healthy",
  "service": "Clip Vault API",
  "timestamp": "2026-07-04 18:30:15"
}
```

---

# Validation

The API performs several validations before creating or updating resources.

- Title cannot be blank.
- Title length must be between **1** and **100** characters.
- Filename is required.
- Filename must have one of the supported video extensions:
  - `.mp4`
  - `.mov`
  - `.avi`
  - `.mkv`
  - `.webm`
- Duplicate filenames are rejected.
- Status must be one of:
  - `uploaded`
  - `processing`
  - `ready`

---

# Running the Project

## 1. Clone the repository

```bash
git clone <repository-url>
cd clipvaultapi
```

---

## 2. Create a virtual environment

### macOS / Linux

```bash
python3 -m venv clipvaultapienv
source clipvaultapienv/bin/activate
```

### Windows

```powershell
python -m venv clipvaultapienv
clipvaultapienv\Scripts\activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Start the API

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

OpenAPI Schema:

```text
http://127.0.0.1:8000/openapi.json
```

---

# Running Tests

Run all tests:

```bash
pytest
```

Run with verbose output:

```bash
pytest -v
```

---

# HTTP Status Codes

| Endpoint | Status |
|----------|--------|
| GET | 200 OK |
| POST | 201 Created |
| PATCH | 200 OK |
| DELETE | 204 No Content |
| Validation Error | 422 Unprocessable Entity |
| Duplicate Filename | 409 Conflict |
| Resource Not Found | 404 Not Found |

---

# Design Decisions

The project was intentionally kept simple while following RESTful API principles and FastAPI best practices.

## SQLite

SQLite was chosen because it is lightweight, requires no additional setup, and satisfies the project requirements.

## SQLAlchemy ORM

SQLAlchemy provides clean object-relational mapping, making database interactions more maintainable and scalable than writing raw SQL.

## Pydantic

Pydantic models handle request validation, response serialization, and automatic API documentation through FastAPI.

## Enum for Clip Status

An enumeration was used to restrict clip status values to:

- uploaded
- processing
- ready

This prevents invalid states from being stored in the database.

## Response Models

Separate response schemas ensure consistent API responses and improve the generated OpenAPI documentation.

## Dependency Injection

Database sessions are managed using FastAPI's dependency injection system, ensuring sessions are created and closed correctly for each request.

## Testing

Pytest was used to implement unit and integration tests covering:

- Health endpoint
- Clip creation
- Duplicate filename validation
- Invalid filename validation
- Retrieve all clips
- Retrieve clip by ID
- Update clip status
- Delete clip
- Not found scenarios

---

# Future Improvements

If this project were expanded further, potential enhancements include:

- Authentication and authorization (JWT/OAuth2)
- Video file upload and storage
- Asynchronous background processing
- Alembic database migrations
- Docker containerization
- Logging and monitoring
- CI/CD pipeline integration
- Search and sorting capabilities
- Cloud storage integration (e.g., AWS S3)

---

# Author

**Anna Ozor**