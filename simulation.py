from sqlalchemy import Column, Integer, String, DateTime, JSON
from datetime import datetime
from app.database import Base
from sqlalchemy import ForeignKey

class Simulation(Base):
    __tablename__ = "simulations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    domain = Column(String, index=True)

    planned_volume = Column(Integer)
    avg_volume = Column(Integer)

    spf = Column(String)
    dmarc = Column(String)
    dkim_status = Column(String)
    dkim_selector = Column(String, nullable=True)

    risk_score = Column(Integer)
    risk_level = Column(String)

    issues = Column(JSON)

    created_at = Column(DateTime, default=datetime.utcnow)
