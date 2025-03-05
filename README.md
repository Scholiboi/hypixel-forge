# Hypixel Forge - Full Stack Project

This project provides a Flask-based backend and a React-based frontend for managing and crafting resources.

## Key Features
- RESTful routes (Flask) to retrieve and modify resources.
- React UI (Create React App) to display and manage resources.
- Crafting and forging items with a React interface calling Flask endpoints.
- Middleware for bridging data (SQLite using SQLAlchemy).

## Setup Instructions

### Backend (Flask)
1. Make sure Python 3 is installed.
2. Create a virtual environment:  
   → python -m venv .venv
3. Activate it:  
   → .venv\Scripts\activate  (Windows)
4. Install dependencies:  
   → pip install -r requirements.txt
5. Initialize database (if needed):  
   → python backend/create_db.py
6. Run the server:  
   → python backend/app.py

### Frontend (React)
1. Navigate to your frontend directory:  
   → cd frontend
2. Install dependencies:  
   → npm install
3. Start the development server:  
   → npm start

## Usage
- Once both servers are running, open http://localhost:3000 to view the React app.
- The Flask server listens by default on http://127.0.0.1:5000.

## Testing
- In the frontend, run:
  → npm test
- Backend routes can be tested with any API client (e.g., Postman).

## Contributing
- Fork this repo and open a pull request for proposed fixes or new features.
