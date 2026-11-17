from fastapi import FastAPI, HTTPException, Query
import asyncio
from database import engine, Base, SessionLocal
import models
import schemas

# Create the database tables if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Webhook Processor",
    description="API for receiving and processing monitoring alerts",
    version="1.0.0"
)


#simple health check endpoint
@app.get("/health")
def health():
    return {"status": "ok"}

################################################

#retrieve all alerts from the database


@app.get("/alerts", response_model=schemas.AlertsPageResponse)
def get_alerts(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100)
):

    db = SessionLocal()

    try:
        # Count all alerts in the database
        total = db.query(models.AlertModel).count()

        # Retrieve only the requested alerts
        alerts = (
            db.query(models.AlertModel)
            .order_by(models.AlertModel.id)
            .offset(skip)
            .limit(limit)
            .all()
        )

        # Calculate total number of pages
        total_pages = (total + limit - 1) // limit

        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "total_pages": total_pages,
            "has_next": skip + len(alerts) < total,
            "has_previous": skip > 0,
            "alerts": alerts
        }

    finally:
        db.close()



################################################

#validates and saves the incoming alert to the database
@app.post("/webhook", response_model=schemas.AlertResponse)
async def receive_webhook(alert: schemas.AlertRequest):

    db = SessionLocal()

    try:
        await asyncio.sleep(3)

        db_alert = models.AlertModel(
            event_id=alert.event_id,
            source=alert.source,
            message=alert.message,
            timestamp=alert.timestamp
        )

        db.add(db_alert)
        db.commit()
        db.refresh(db_alert) #fetching auto generated id and other fields from the database

        return db_alert
    
    except HTTPException:
        raise


    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process alert: {str(e)}"
        )

    finally:
        db.close()