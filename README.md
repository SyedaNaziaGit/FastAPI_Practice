# FastAPI Practice: Patient Management API

A hands-on FastAPI project that builds a REST API for managing patient records. It covers the core FastAPI and Pydantic skills needed before wrapping ML or AI models in an API: request validation, path and query parameters, computed fields, and full CRUD operations.

## Features

- Full **CRUD** on patient records, stored in a JSON file
- **Pydantic validation** (age range, positive height and weight, allowed gender values)
- **Computed fields:** BMI and a health verdict are calculated automatically
- **Sorting** patients by height, weight, or BMI
- **Partial updates** with a separate update model
- Proper **HTTP errors** (400 and 404) with clear messages
- Auto-generated interactive docs (Swagger UI)

## API endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Welcome message |
| GET | `/view` | List all patients |
| GET | `/patient/{patient_id}` | Get one patient by ID (404 if not found) |
| GET | `/sort?sort_by=bmi&order=desc` | Sort patients by `height`, `weight`, or `bmi` (`asc` or `desc`) |
| POST | `/create` | Create a new patient |
| PUT | `/edit?patient_id=P001` | Update any subset of a patient's fields |
| DELETE | `/delete/{patient_id}` | Delete a patient |

## Data model

| Field | Type | Rules |
|-------|------|-------|
| `id` | string | Required, for example `P001` |
| `name` | string | Required |
| `city` | string | Required |
| `age` | integer | Greater than 0 and less than 120 |
| `gender` | string | `male`, `female`, or `others` |
| `height` | float | Metres, greater than 0 |
| `weight` | float | Kilograms, greater than 0 |
| `bmi` | float | **Computed:** `weight / height²`, rounded to 2 decimals |
| `verdict` | string | **Computed** from BMI (see below) |

**BMI verdict**

| BMI | Verdict |
|-----|---------|
| Below 18.5 | Under Weight |
| 18.5 to 24.9 | Normal |
| 25 to 29.9 | Over Weight |
| 30 and above | Obese |

## Tech stack

- **Python** 3.10 or higher
- **FastAPI** for the web framework
- **Pydantic v2** for validation and computed fields
- **Uvicorn** as the ASGI server
- **JSON file** (`patients.json`) as a simple data store

## Project structure

```
FastAPI_Practice/
├── main.py            # API routes and Pydantic models
├── patients.json      # Patient data store
└── README.md
```

## Getting started

### Installation

```bash
git clone https://github.com/SyedaNaziaGit/FastAPI_Practice.git
cd FastAPI_Practice
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install fastapi "uvicorn[standard]" "pydantic>=2"
```

### Run the server

```bash
uvicorn main:app --reload
```

- API: `http://127.0.0.1:8000`
- Interactive docs (Swagger UI): `http://127.0.0.1:8000/docs`

## Example requests

**Create a patient**

```bash
curl -X POST http://127.0.0.1:8000/create \
  -H "Content-Type: application/json" \
  -d '{"id":"P010","name":"Asha","city":"Bengaluru","age":29,"gender":"female","height":1.62,"weight":58}'
```

**Sort by BMI, highest first**

```bash
curl "http://127.0.0.1:8000/sort?sort_by=bmi&order=desc"
```

**Update only the weight**

```bash
curl -X PUT "http://127.0.0.1:8000/edit?patient_id=P010" \
  -H "Content-Type: application/json" \
  -d '{"weight":60}'
```

BMI and verdict are recalculated automatically after the update.

## What I learned

- Defining request and response models with Pydantic, including constraints with `Field`
- Using `@computed_field` so derived values stay consistent
- Path
