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

---
### Concepts:

What is an API?
APIs are mechanisms that enable two software components—such as the frontend and backend of an application—to communicate with each other using a defined set of rules, protocols, and data formats
<img width="615" height="221" alt="image" src="https://github.com/user-attachments/assets/b73c98ac-cec8-46a5-85de-c901591a60fe" />

<img width="975" height="573" alt="image" src="https://github.com/user-attachments/assets/31bedaa2-6a1e-4a52-b873-b8cc08a8bb49" />

<img width="975" height="535" alt="image" src="https://github.com/user-attachments/assets/aa3e8419-e02f-4e46-a134-bd5fd3c2e0e2" />
<img width="975" height="560" alt="image" src="https://github.com/user-attachments/assets/9977da1a-7649-4eb8-9348-b749e6b5bc37" />

<img width="975" height="585" alt="image" src="https://github.com/user-attachments/assets/e4d84dad-97ac-49df-9c78-42c6e9dfa5a3" />

<img width="975" height="479" alt="image" src="https://github.com/user-attachments/assets/ce719c69-19c0-45c3-ac90-b996a7fc157a" />

<img width="975" height="536" alt="image" src="https://github.com/user-attachments/assets/31e7d704-3403-448f-8770-ef27ea3cbce0" />

<img width="975" height="535" alt="image" src="https://github.com/user-attachments/assets/1d2f4b05-6c7d-419b-b8da-40ac76d993c0" />

<img width="975" height="503" alt="image" src="https://github.com/user-attachments/assets/8aec81ed-3fbc-44df-978e-e908066020cb" />

<img width="957" height="151" alt="image" src="https://github.com/user-attachments/assets/2d57b4c7-4f79-40e3-93d9-43f141da6cc6" />

<img width="975" height="511" alt="image" src="https://github.com/user-attachments/assets/e0b044eb-b48f-4c42-a476-086c73aeded3" />

<img width="669" height="253" alt="image" src="https://github.com/user-attachments/assets/47493d3f-8ee7-4474-8dec-f76e56cec8da" />

<img width="873" height="230" alt="image" src="https://github.com/user-attachments/assets/9e2dd741-7bd6-48d2-822b-092b1fa1a938" />

### Why FastAPI is fast to code?

1. Automatic Input Validation

2. Auto-Generated Interactive Documentation

3. Seamless Integration with Modern Ecosystem (ML/DL libraries, OAuth, JWT, SQL Alchemy, Docker, Kubernetes etc.)

### Path Params

Path parameters are dynamic segments of a URL path used to identify a specific resource.

The Path() function in FastAPI is used to provide metadata, validation rules, and documentation hints for path parameters in your API endpoints.

Title

Description

Example

ge, gt, le, lt

Min_length

Max_length

regex

HTTP status codes are 3-digit numbers returned by a web server (like FastAPI) to indicate the result of a client's request (like from a browser or API consumer).

They help the client (browser, frontend, mobile app, etc.) understand:

• whether the request was successful,

• whether something went wrong,

• and what kind of issue occurred (if any).

2xx | Success | The request was successfully received and processed

3xx | Redirection | Further action needs to be taken (e.g., redirect)

4xx | Client Error | Something is wrong with the request from the client

<img width="975" height="633" alt="image" src="https://github.com/user-attachments/assets/ea0c892c-3eec-4fb0-9c9f-b72c84232e9d" />

<img width="975" height="390" alt="image" src="https://github.com/user-attachments/assets/05c99403-af43-44de-92ae-44c67bdf47d5" />

HTTPException is a special built-in exception in FastAPI used to return custom HTTP error responses when something goes wrong in your API.

Instead of returning a normal JSON or crashing the server, you can gracefully raise an error with:

• a proper HTTP status code (like 404, 400, 403, etc.)

• a custom error message

• (optional) extra headers

### Query Parameter

Query parameters are optional key-value pairs appended to the end of a URL, used to pass additional data to the server in an HTTP request. They are typically employed for operations like filtering, sorting, searching, and pagination, without altering the endpoint path itself.

/patients?city=Delhi&sort_by=age

• The ? marks the start of query parameters.

• Each parameter is a key-value pair: key=value

• Multiple parameters are separated by &

In this case:

• city=Delhi is a query parameter for filtering

• sort_by=age is a query parameter for sorting

Query() is a utility function provided by FastAPI to declare, validate, and document query parameters in your API endpoints.

A request body is the portion of an HTTP request that contains data sent by the client to the server. It is typically used in HTTP methods such as POST, or PUT to transmit structured data (e.g., JSON, XML, form-data) for the purpose of creating or updating resources on the server. The server parses the request body to extract the necessary information and perform the intended operation.

### Pydantic

1. Define a Pydantic model that represents the ideal schema of the data.
	
  • This includes the expected fields, their types, and any validation constraints (e.g., gt=0 for positive numbers).

2. Instantiate the model with raw input data (usually a dictionary or JSON-like structure).

  • Pydantic will automatically validate the data and coerce it into the correct Python types (if possible).
	
  • If the data doesn't meet the model's requirements, Pydantic raises a ValidationError.

3. Pass the validated model object to functions or use it throughout your codebase.

  • This ensures that every part of your program works with clean, type-safe, and logically valid data.
---
