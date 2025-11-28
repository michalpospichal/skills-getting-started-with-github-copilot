# Copilot Instructions for Mergington High School Activities API

## Project Overview

This is a **FastAPI-based web application** for a high school activities management system. The project demonstrates a full-stack implementation with a Python backend API and vanilla JavaScript frontend, all serving static files from a single server.

**Key Files:**
- `src/app.py` - Main FastAPI application with in-memory activity database
- `src/static/` - Frontend HTML, CSS, and JavaScript
- `requirements.txt` - Python dependencies (FastAPI, uvicorn)

## Architecture & Data Flow

### Backend Structure (src/app.py)

- **In-memory database**: All activities and participant data stored in a Python dictionary (`activities`) that resets on server restart
- **Activity data model**: Each activity has `description`, `schedule`, `max_participants`, and `participants` (list of email strings)
- **API endpoints**:
  - `GET /activities` - Returns entire activities dictionary
  - `POST /activities/{activity_name}/signup?email={student_email}` - Appends email to participants list

### Frontend Architecture

- **Static file serving**: All frontend files mounted at `/static` via FastAPI's StaticFiles
- **Root redirect**: `GET /` redirects to `/static/index.html`
- **Data flow**: `app.js` fetches activities on page load, populates HTML dynamically, handles form submission to signup endpoint
- **Error handling**: Frontend catches fetch errors and displays user-friendly messages; API returns JSON with `detail` field on errors

## Development Workflow

### Running the Application

```bash
# Install dependencies
pip install fastapi uvicorn

# Start server (runs on http://localhost:8000)
python src/app.py
```

### Testing

- `pytest.ini` is configured with `pythonpath = .` to enable imports from workspace root
- No test files exist yet; tests should import from `src.app` module

### Making Changes

**Backend changes**: Modify `src/app.py` endpoints, activities data, or validation logic. Server requires restart.

**Frontend changes**: Modify `src/static/app.js` (logic), `index.html` (structure), or `styles.css` (styling). Changes are live without restart due to static file serving.

## Patterns & Conventions

### Error Handling

- **Backend**: Use `HTTPException(status_code=404, detail="message")` for validation failures (e.g., activity not found)
- **Frontend**: Wrap API calls in try-catch; display errors to users via `messageDiv` with `.error` class; errors auto-hide after 5 seconds

### Data Validation Gaps (Known Limitations)

- No check if student is already signed up (duplicates allowed)
- No check if activity is full (exceeds max_participants)
- All data is in-memory and lost on server restart
- Consider adding these validations when extending the API

### Naming Conventions

- Activities identified by name (string key) - not a separate ID field
- Students identified by email addresses
- All API responses return raw data structures (not wrapped in `data` or `result` fields)

## Key Integration Points

- **FastAPI conventions**: Use path parameters for resource identifiers (`{activity_name}`), query parameters for options (`?email=`)
- **Frontend-backend contract**: Frontend depends on `/activities` returning a dictionary keyed by activity name with `max_participants` and `participants` fields; changing this structure breaks the UI
- **Static file paths**: Assets referenced via `/static/` prefix (e.g., `/static/app.js`); ensure paths in HTML match actual file locations

## Quick Reference Commands

| Task | Command |
|------|---------|
| Install deps | `pip install -r requirements.txt` |
| Run server | `python src/app.py` |
| Access API docs | `http://localhost:8000/docs` |
| Access app | `http://localhost:8000` |
