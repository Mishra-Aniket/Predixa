from sqlalchemy import Column, Integer, Float, DateTime
from datetime import datetime
from .database import Base

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    days_ahead = Column(Integer)
    predicted_price = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
