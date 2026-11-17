
from sqlalchemy import Column, Integer, String, DateTime
from database import Base

class AlertModel(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(String, nullable=False)
    source = Column(String, nullable=False)
    message = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    status = Column(String, default="processed")
