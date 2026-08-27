from fastapi import FastAPI, Depends, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

import sys
import os

from pydantic import BaseModel
from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, Session


# =========================================================
# DATABASE
# =========================================================

DATABASE_URL = "postgresql+psycopg://postgres:root@localhost:5432/urban_intelligence"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


class TrafficRecord(Base):
    __tablename__ = "traffic_records"

    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String(50), nullable=False)
    timestamp = Column(DateTime, nullable=False)
    cars = Column(Integer, nullable=False)
    motorcycles = Column(Integer, nullable=False)
    buses = Column(Integer, nullable=False)
    trucks = Column(Integer, nullable=False)
    total_vehicles = Column(Integer, nullable=False)
    traffic_level = Column(String(20), nullable=False)


Base.metadata.create_all(bind=engine)


# =========================================================
# DATABASE SESSION
# =========================================================

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# =========================================================
# FASTAPI
# =========================================================

app = FastAPI()


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# AI IMPORT
# =========================================================

AI_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "ai",
        "src"
    )
)

sys.path.append(AI_PATH)

from traffic_density import analyze_video


# =========================================================
# UPLOAD DIRECTORY
# =========================================================

UPLOAD_DIR = os.path.join(
    os.path.dirname(__file__),
    "uploads"
)

os.makedirs(UPLOAD_DIR, exist_ok=True)


# =========================================================
# TRAFFIC DATA MODEL
# =========================================================

class TrafficData(BaseModel):
    event_type: str
    timestamp: datetime
    cars: int
    motorcycles: int
    buses: int
    trucks: int
    total_vehicles: int
    traffic_level: str


# =========================================================
# ROOT
# =========================================================

@app.get("/")
def root():
    return {
        "message": "Traffic Monitoring Backend is running"
    }


# =========================================================
# SAVE TRAFFIC DATA
# =========================================================

@app.post("/traffic")
def receive_traffic(
    data: TrafficData,
    db: Session = Depends(get_db)
):

    traffic = TrafficRecord(
        event_type=data.event_type,
        timestamp=data.timestamp,
        cars=data.cars,
        motorcycles=data.motorcycles,
        buses=data.buses,
        trucks=data.trucks,
        total_vehicles=data.total_vehicles,
        traffic_level=data.traffic_level
    )

    db.add(traffic)
    db.commit()
    db.refresh(traffic)

    return traffic


# =========================================================
# GET TRAFFIC HISTORY
# =========================================================

@app.get("/traffic")
def get_traffic(
    db: Session = Depends(get_db)
):

    records = db.query(TrafficRecord).all()

    return records


# =========================================================
# UPLOAD + AI ANALYSIS
# =========================================================

@app.post("/analyze-video")
async def analyze_uploaded_video(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    # -----------------------------------------------------
    # 1. Check file
    # -----------------------------------------------------

    if not file.filename:
        return {
            "error": "No video file selected"
        }


    # -----------------------------------------------------
    # 2. Create safe filename
    # -----------------------------------------------------

    filename = os.path.basename(file.filename)

    file_path = os.path.join(
        UPLOAD_DIR,
        filename
    )


    # -----------------------------------------------------
    # 3. Save uploaded video
    # -----------------------------------------------------

    with open(file_path, "wb") as buffer:

        content = await file.read()

        buffer.write(content)


    print()
    print("======================================")
    print("VIDEO UPLOAD")
    print("======================================")
    print("Filename:", filename)
    print("Saved to:", file_path)
    print("======================================")


    # -----------------------------------------------------
    # 4. SEND VIDEO TO AI
    # -----------------------------------------------------

    result = analyze_video(file_path)


    # -----------------------------------------------------
    # 5. SAVE AI RESULT TO DATABASE
    # -----------------------------------------------------

    traffic = TrafficRecord(
        event_type=result["event_type"],
        timestamp=datetime.fromisoformat(
            result["timestamp"]
        ),
        cars=result["cars"],
        motorcycles=result["motorcycles"],
        buses=result["buses"],
        trucks=result["trucks"],
        total_vehicles=result["total_vehicles"],
        traffic_level=result["traffic_level"]
    )

    db.add(traffic)

    db.commit()

    db.refresh(traffic)


    # -----------------------------------------------------
    # 6. RETURN RESULT TO FRONTEND
    # -----------------------------------------------------

    return {
        "id": traffic.id,
        "event_type": traffic.event_type,
        "timestamp": traffic.timestamp,
        "cars": traffic.cars,
        "motorcycles": traffic.motorcycles,
        "buses": traffic.buses,
        "trucks": traffic.trucks,
        "total_vehicles": traffic.total_vehicles,
        "traffic_level": traffic.traffic_level
    }