# Secure TinyDB App

This project provides a small FastAPI application that stores uploaded data in a local TinyDB database. It supports image uploads and CSV imports, and uses session-based authentication.

## Features

- Login/logout using a single admin account
- Passwords verified with `passlib[bcrypt]`
- Session middleware for authentication
- Upload images to `static/images/` and store metadata in `db.json`
- Upload CSV files to insert multiple records
- Dashboard listing all stored entries with image previews
- Docker support

## Setup

1. Copy `.env.example` to `.env` and adjust the values.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the server:
   ```bash
   python run.py
   ```

The application will be available at `http://localhost:8000`.

## Docker

To build and run with Docker:

```bash
docker build -t secure-tinydb-app .
docker run -p 8000:8000 secure-tinydb-app
```

## Docker Compose

To start the application with Docker Compose:

```bash
docker compose up --build
```

The compose file loads variables from `.env` and persists the database and uploaded images in the current directory.
