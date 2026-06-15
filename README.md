# Athlete QR Identification System

## Overview

The Athlete QR Identification System is a FastAPI-based backend application that enables athlete registration, QR code generation, and secure athlete identification using QR tokens. Athlete information is stored in a Supabase PostgreSQL database, while unique QR codes are generated for each athlete.

The system allows event organizers, coaches, and administrators to quickly identify athletes by scanning their QR codes and retrieving their profiles from the database.

---

## Features

* Athlete Registration
* Secure UUID Token Generation
* QR Code Generation
* Supabase Database Integration
* Athlete Profile Retrieval by QR Token
* QR Code Download Endpoint
* REST API with FastAPI
* Interactive Swagger Documentation

---

## Technology Stack

### Backend

* FastAPI
* Python

### Database

* Supabase PostgreSQL

### Libraries

* supabase-py
* qrcode
* python-dotenv
* uvicorn
* pydantic

---

## Database Schema

### user_profiles

| Column     | Type      |
| ---------- | --------- |
| user_id    | UUID      |
| user_name  | TEXT      |
| dob        | DATE      |
| gender     | TEXT      |
| sport      | TEXT      |
| team_club  | TEXT      |
| height     | NUMERIC   |
| weight     | NUMERIC   |
| qr_token   | TEXT      |
| created_at | TIMESTAMP |

### scan_events

| Column     | Type      |
| ---------- | --------- |
| id         | UUID      |
| athlete_id | UUID      |
| scanned_at | TIMESTAMP |
| location   | TEXT      |
| event_name | TEXT      |

---

## API Endpoints

### Health Check

#### GET /

Returns API status.

#### GET /health

Returns health status.

---

### Athlete Management

#### POST /athletes

Register a new athlete and generate a QR code.

Example Request:

```json
{
  "user_name": "ABC",
  "dob": "2003-05-15",
  "gender": "Female",
  "sport": "Athletics",
  "team_club": "PCCOE",
  "height": 165,
  "weight": 55
}
```

---

#### GET /athletes/token/{token}

Retrieve athlete details using a QR token.

---

#### GET /athletes/{athlete_id}/qr

Download the athlete QR code image.

---

## System Workflow

1. Register Athlete
2. Generate Unique UUID Token
3. Store Athlete Data in Supabase
4. Generate QR Code containing Token
5. Scan QR Code
6. Retrieve Token
7. Fetch Athlete Profile from Database
8. Display Athlete Information

---

## Project Structure

```text
QR_Generation/
│
├── main.py
├── athlete.py
├── athletes.py
├── qr.py
├── qr_service.py
├── supabase_service.py
├── token_utils.py
├── requirements.txt
├── .env
├── generated_qr/
└── README.md
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/Siyakale94/QR_Generation.git
cd QR_Generation
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file:

```env
SUPABASE_URL=your_supabase_url
SUPABASE_SERVICE_KEY=your_service_role_key
QR_OUTPUT_DIR=generated_qr
```

### Run Application

```bash
uvicorn main:app --reload
```

---

## API Documentation

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

---

## Future Enhancements

* Frontend Dashboard
* Athlete Photo Upload
* Supabase Storage Integration
* Scan History Tracking
* Event Management Module
* Role-Based Authentication
* Cloud Deployment

---

## Author

**Siya Kale**

Pimpri Chinchwad College of Engineering (PCCOE)

Department of Computer Science and Engineering (Comp Regional)
