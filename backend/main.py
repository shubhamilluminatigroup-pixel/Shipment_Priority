from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import List
from database import SessionLocal, engine
import models
import schemas
from schemas import ShipmentCreate, FixedWeightConfig, WeightConfigItem
  

from priority_model import calculate_priority_scores
from fastapi.middleware.cors import CORSMiddleware

# Create tables
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI
app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# insert weight data
@app.post("/weights/fixed/")
def update_fixed_weights(config: FixedWeightConfig, db: Session = Depends(get_db)):
    # ✅ Clear all existing weights
    db.query(models.WeightConfig).delete()

    # ✅ Add new weights from the provided config
    new_weights = [
        models.WeightConfig(feature_name=feature, weight_value=value)
        for feature, value in config.dict().items()
    ]

    db.add_all(new_weights)
    db.commit()
    return {"message": "Weights overwritten successfully."}

# get all weights
@app.get("/weights/get", response_model=list[WeightConfigItem])
def get_all_weights(db: Session = Depends(get_db)):
    return db.query(models.WeightConfig).all()


# 🚀 BULK INSERT ENDPOINT
@app.post("/shipments/bulk/")
def create_bulk_shipments(shipments: List[ShipmentCreate], db: Session = Depends(get_db)):
    shipment_objs = [models.Shipment(**shipment.dict()) for shipment in shipments]
    db.add_all(shipment_objs)
    db.commit()
    return {"message": f"{len(shipment_objs)} shipments inserted successfully"}

# ✅ GET all shipments
@app.get("/shipments/", response_model=List[schemas.Shipment])
def get_all_shipments(db: Session = Depends(get_db)):
    return db.query(models.Shipment).all()

# calculate priority scores
@app.post("/shipments/score/")
def calculate_and_update_priority_scores(db: Session = Depends(get_db)):
    shipments = db.query(models.Shipment).all()

    if not shipments:
        return {"message": "No shipments found."}

    scoring_input = []
    for s in shipments:
        scoring_input.append({
            "value": s.value,
            "weight": s.weight,
            "volume": s.volume,
            "shelf_life_days": s.shelf_life_days,
            "delivery_date": s.delivery_date
        })

    scores = calculate_priority_scores(scoring_input, db)

    for shipment, score in zip(shipments, scores):
        shipment.priority_score = float(score)

    db.commit()
    return {"message": f"Updated {len(scores)} shipments with priority scores."}


# ✅ Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
