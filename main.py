import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from database import create_document, get_documents, db
from schemas import Job, ContactMessage

app = FastAPI(title="Staff Arabia API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Staff Arabia API running"}

@app.get("/api/hello")
def hello():
    return {"message": "Hello from Staff Arabia backend!"}

# Jobs endpoints
@app.get("/api/jobs")
def list_jobs(category: Optional[str] = None, location: Optional[str] = None, type: Optional[str] = None, limit: int = 12):
    if db is None:
        raise HTTPException(status_code=500, detail="Database not connected")
    filters = {}
    if category:
        filters["category"] = category
    if location:
        filters["location"] = location
    if type:
        filters["type"] = type
    jobs = get_documents("job", filters, limit)
    # Convert ObjectId to string
    for j in jobs:
        j["_id"] = str(j.get("_id"))
    return {"items": jobs}

class JobCreate(Job):
    pass

@app.post("/api/jobs")
def create_job(payload: JobCreate):
    try:
        inserted_id = create_document("job", payload)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Contact endpoint
class ContactCreate(ContactMessage):
    pass

@app.post("/api/contact")
def submit_contact(payload: ContactCreate):
    try:
        inserted_id = create_document("contactmessage", payload)
        return {"id": inserted_id, "status": "received"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
            
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    
    # Check environment variables
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    
    return response

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
