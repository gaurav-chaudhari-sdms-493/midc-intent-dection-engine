from fastapi import FastAPI

app = FastAPI(
    title="MIDC Enterprise Intent Detection Engine",
    version="0.1.0",
    description="Enterprise AI-powered Investor Inquiry Management System",
)

@app.get("/")
def root():
    return {
        "message": "MIDC Intent Detection Engine API",
        "status": "running"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }
