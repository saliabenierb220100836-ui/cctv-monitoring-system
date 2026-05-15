# KAFKAM — CCTV Monitoring System

A web-based CCTV monitoring dashboard built with Flask. Designed for real-time IP camera surveillance with user authentication and activity tracking.

## Features
- 🔐 Login / Logout with session management
- 📷 Live IP camera feed via snapshot refresh
- 📋 Activity logs with device detection
- ⚙️ Account settings (change username & password)
- 🕐 Philippine Standard Time (PHT) timestamps

## Tech Stack
- **Backend:** Python, Flask, SQLAlchemy, Flask-Login
- **Frontend:** Jinja2, Tailwind CSS
- **Database:** SQLite (local) / PostgreSQL (Railway)
- **Deployment:** Railway

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Run the app: `python run.py`
3. Initialize database: visit `/setup-database-xyz`
4. Login with `admin` / `admin123`

## Environment Variables
| Variable | Description |
|---|---|
| `SECRET_KEY` | Flask secret key |
| `CAMERA_URL` | IP camera snapshot URL |
| `CAMERA_NAME` | Display name of the camera |
