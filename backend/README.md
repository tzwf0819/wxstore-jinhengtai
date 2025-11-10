# Jinhengtai Mall FastAPI Backend

## Overview

This backend service provides REST APIs for the Jinhengtai mini program mall. It is built with FastAPI and connects to a remote Microsoft SQL Server instance hosted at `152.136.13.33:1433`.

## Project Structure

```
backend/
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes/
│   │       └── health.py
│   ├── core/
│   │   ├── config.py
│   │   └── database.py
│   ├── __init__.py
│   └── main.py
├── tests/
│   ├── conftest.py
│   └── test_health.py
├── .env.example
├── .gitignore
├── requirements.txt
├── pyproject.toml
└── README.md
```

## Setup

1. **Create virtual environment**
   ```powershell
   cd d:\Yida\code\jinhengtai\cloudbase\backend
   py -3 -m venv .venv
   .\.venv\Scripts\activate
   ```

2. **Install dependencies**
   ```powershell
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   - Copy `.env.example` to `.env`
   - Update the SQL Server credentials if needed

4. **Run tests**
   ```powershell
   pytest
   ```

5. **Run development server**
   ```powershell
   uvicorn app.main:app --reload
   ```

## Health Check

`GET /health/ping` verifies application status and database connectivity.
