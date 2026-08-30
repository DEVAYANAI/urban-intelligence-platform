# 🚦 Urban Intelligence Platform

An AI-powered traffic monitoring system that analyzes uploaded traffic videos using YOLO11s and displays vehicle statistics, traffic levels, and road event information through a web dashboard.

---

## 📌 Features

- Upload traffic videos through the web interface
- Detect cars, motorcycles, buses, and trucks
- Track objects using ByteTrack
- Analyze traffic density
- Classify traffic as LOW, MEDIUM, or HIGH
- Detect large gatherings based on person detection
- Generate road event alerts
- Store analysis results in PostgreSQL
- Display results in a React dashboard
- Generate an annotated output video

---

## 🛠️ Technologies Used

### Frontend

- React
- Vite
- CSS

### Backend

- FastAPI
- SQLAlchemy
- PostgreSQL

### AI

- YOLO11s
- ByteTrack
- Ultralytics

---

## 🔄 Project Workflow

```text
User uploads a traffic video
        ↓
React Frontend
        ↓
FastAPI Backend
        ↓
AI Module
(YOLO11s + ByteTrack)
        ↓
Vehicle and Person Detection
        ↓
Traffic Density Analysis
        ↓
Road Event Analysis
        ↓
PostgreSQL Database
        ↓
Results displayed on Dashboard
```

---

## 🚀 How to Run This Project

To run this project locally:

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd urban-intelligence

2. Set up PostgreSQL

Install PostgreSQL and create an empty database:

CREATE DATABASE urban_intelligence;

Create a .env file inside the backend folder and add your PostgreSQL connection:

DATABASE_URL=postgresql+psycopg://postgres:YOUR_POSTGRES_PASSWORD@localhost:5432/urban_intelligence

Replace YOUR_POSTGRES_PASSWORD with your own PostgreSQL password.

The required database tables are automatically created when the backend starts.

3. Run the Backend

Open Terminal 1:

cd backend
python -m venv venv

Activate the virtual environment:

Windows:

venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Run the backend:

uvicorn main:app --reload

The backend will run at:

http://localhost:8000
4. Run the Frontend

Open Terminal 2:

cd frontend
npm install
npm run dev

Open the URL shown in the terminal, usually:

http://localhost:5173

Use the Application
1. Open the frontend in your browser.
2. Upload a traffic video.
3. The video is sent to the FastAPI backend.
4. YOLO analyzes the video.
5. Traffic and road event results are stored in PostgreSQL.
6. The results are displayed on the dashboard.
```
