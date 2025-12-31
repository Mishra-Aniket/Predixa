from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder

import joblib
import numpy as np
import os

from sqlalchemy.orm import Session
from db.database import SessionLocal
from db.models import Prediction

# ================== APP INIT ==================
app = FastAPI(
    title="Predixa API",
    redirect_slashes=False  # ✅ CRITICAL: avoids 302 redirect
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # tighten later if needed
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ================== MODEL LOAD ==================
MODEL_PATH = "model/price_model.pkl"

if not os.path.exists(MODEL_PATH):
    raise RuntimeError("❌ ML model not found. Train it first.")

model = joblib.load(MODEL_PATH)

# ================== DB DEP ==================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ================== ROUTES ==================
@app.get("/")
def home():
    return {"message": "Predixa API is running 🚀"}

# ---------- PREDICT ----------
@app.get("/predict")
def predict(days: int, db: Session = Depends(get_db)):
    try:
        if days <= 0:
            raise HTTPException(status_code=400, detail="Days must be > 0")

        prediction_value = model.predict(
            np.array([[days]])
        )[0]

        record = Prediction(
            days_ahead=days,
            predicted_price=float(prediction_value)
        )

        db.add(record)
        db.commit()
        db.refresh(record)

        return {
            "days_ahead": days,
            "predicted_price": round(float(prediction_value), 2),
            "saved": True
        }

    except HTTPException:
        raise
    except Exception as e:
        print("❌ BACKEND ERROR:", e)
        raise HTTPException(
            status_code=500,
            detail="Prediction failed"
        )

# ---------- HISTORY ----------
@app.get("/history")
def history(db: Session = Depends(get_db)):
    records = (
        db.query(Prediction)
        .order_by(Prediction.created_at.desc())
        .all()
    )
    return jsonable_encoder(records)
