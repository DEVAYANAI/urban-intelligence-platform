from fastapi import FastAPI, Depends
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, Session

DATABASE_URL = "postgresql+psycopg://postgres:kayal@localhost:5432/urban_intelligence"

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


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()


class TrafficData(BaseModel):
    event_type: str
    timestamp: datetime
    cars: int
    motorcycles: int
    buses: int
    trucks: int
    total_vehicles: int
    traffic_level: str


@app.get("/")
def root():
    return {"message": "Traffic Monitoring Backend is running"}


@app.post("/traffic")
def receive_traffic(data: TrafficData, db: Session = Depends(get_db)):
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

@app.get("/traffic")
def get_traffic(db: Session = Depends(get_db)):
    records = db.query(TrafficRecord).all()
    return records