from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from athletes import router as athletes_router
from qr import router as qr_router

app = FastAPI(
    title="Athlete QR Identification System",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(athletes_router)
app.include_router(qr_router)

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/health")
def health():
    return {"status": "healthy"}