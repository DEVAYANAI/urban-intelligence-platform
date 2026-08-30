from fastapi import FastAPI, Depends, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

import sys
import os

from pydantic import BaseModel
from datetime import datetime

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    DateTime,
    Float,
    Boolean
)

from sqlalchemy.orm import (
    sessionmaker,
    declarative_base,
    Session
)


# =========================================================
# DATABASE
# =========================================================

import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
print("DATABASE URL:", DATABASE_URL)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


# =========================================================
# DATABASE TABLE
# =========================================================

class TrafficRecord(Base):

    __tablename__ = "traffic_records"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    event_type = Column(
        String(50),
        nullable=False
    )

    timestamp = Column(
        DateTime,
        nullable=False
    )

    cars = Column(
        Integer,
        nullable=False
    )

    motorcycles = Column(
        Integer,
        nullable=False
    )

    buses = Column(
        Integer,
        nullable=False
    )

    trucks = Column(
        Integer,
        nullable=False
    )

    total_vehicles = Column(
        Integer,
        nullable=False
    )

    traffic_level = Column(
        String(20),
        nullable=False
    )


    # =====================================================
    # ROAD EVENT FIELDS
    # =====================================================

    road_event_detected = Column(
        Boolean,
        nullable=False,
        default=False
    )

    road_event_type = Column(
        String(100),
        nullable=True
    )

    road_event_confidence = Column(
        Float,
        nullable=False,
        default=0.0
    )

    alert_message = Column(
        String(500),
        nullable=True
    )


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

    allow_headers=["*"]
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

import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AI_SRC_PATH = os.path.join(PROJECT_ROOT, "ai", "src")

sys.path.append(AI_SRC_PATH)

from traffic_density import analyze_video

# =========================================================
# UPLOAD DIRECTORY
# =========================================================

UPLOAD_DIR = os.path.join(

    os.path.dirname(__file__),

    "uploads"
)

os.makedirs(

    UPLOAD_DIR,

    exist_ok=True
)


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


    # ROAD EVENT DATA

    road_event_detected: bool = False

    road_event_type: str | None = None

    road_event_confidence: float = 0.0

    alert_message: str | None = None


# =========================================================
# ROOT
# =========================================================

@app.get("/")

def root():

    return {

        "message": "Traffic Monitoring Backend is running"

    }


# =========================================================
# SAVE TRAFFIC DATA MANUALLY
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

        traffic_level=data.traffic_level,


        road_event_detected=data.road_event_detected,

        road_event_type=data.road_event_type,

        road_event_confidence=data.road_event_confidence,

        alert_message=data.alert_message
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

    records = db.query(

        TrafficRecord

    ).all()


    return records


# =========================================================
# UPLOAD VIDEO + AI ANALYSIS
# =========================================================

@app.post("/analyze-video")

async def analyze_uploaded_video(

    file: UploadFile = File(...),

    db: Session = Depends(get_db)
):


    # -----------------------------------------------------
    # CHECK FILE
    # -----------------------------------------------------

    if not file.filename:

        return {

            "error": "No video file selected"

        }


    # -----------------------------------------------------
    # SAFE FILENAME
    # -----------------------------------------------------

    filename = os.path.basename(

        file.filename

    )

    file_path = os.path.join(

        UPLOAD_DIR,

        filename

    )


    # -----------------------------------------------------
    # SAVE VIDEO
    # -----------------------------------------------------

    with open(

        file_path,

        "wb"

    ) as buffer:

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
    # SEND VIDEO TO AI
    # -----------------------------------------------------

    result = analyze_video(file_path)


    # -----------------------------------------------------
    # SAVE AI RESULT TO DATABASE
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

        traffic_level=result["traffic_level"],


        # ROAD EVENT DATA

        road_event_detected=result.get(
            "road_event_detected",
            False
        ),

        road_event_type=result.get(
            "road_event_type",
            None
        ),

        road_event_confidence=result.get(
            "road_event_confidence",
            0.0
        ),

        alert_message=result.get(
            "alert_message",
            "No road event detected. Route is currently clear."
        )
    )


    db.add(traffic)

    db.commit()

    db.refresh(traffic)


    # -----------------------------------------------------
    # RETURN RESULT TO FRONTEND
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

        "traffic_level": traffic.traffic_level,


        # ROAD EVENT RESPONSE

        "road_event_detected":
            traffic.road_event_detected,

        "road_event_type":
            traffic.road_event_type,

        "road_event_confidence":
            traffic.road_event_confidence,

        "alert_message":
            traffic.alert_message
    }