from fastapi import FastAPI
from app.routers.persistence import router as persistence
from app.routers.post_scan import router as post_scan
from app.routers.get_scan import router as get_scan
from app.routers.get_html import router as get_html

app = FastAPI()

app.title = "Meli API With FastAPI"
app.version = "1.0.0"

# Endpoints
app.include_router(persistence)
app.include_router(post_scan)
app.include_router(get_scan)
app.include_router(get_html)

@app.get("/")
def status():
    return {"Online"}