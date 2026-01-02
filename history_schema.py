from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class SimulationHistoryItem(BaseModel):
    id: int
    domain: str
    risk_score: int
    risk_level: str
    spf: str
    dmarc: str
    dkim_status: str
    created_at: datetime

class SimulationHistoryResponse(BaseModel):
    total: int
    items: List[SimulationHistoryItem]
