from pydantic import BaseModel
from datetime import datetime


# Request DTO
class AlertRequest(BaseModel):
    event_id: str
    source: str
    message: str
    timestamp: datetime


# Response DTO
class AlertResponse(BaseModel):
    id: int
    event_id: str
    source: str
    message: str
    timestamp: datetime
    status: str

    model_config = {
        "from_attributes": True
    }


class AlertsPageResponse(BaseModel):
    total: int
    skip: int
    limit: int
    total_pages: int
    has_next: bool
    has_previous: bool
    alerts: list[AlertResponse]
