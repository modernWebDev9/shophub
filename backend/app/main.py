from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.api import auth, products

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="E-Commerce API", version="1.0.0", docs_url="/docs", redoc_url="/redoc")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(products.router)

@app.get("/")
def root():
    return {"message": "E-Commerce API is running!", "version": "1.0.0"}

@app.get("/health")
def health():
    return {"status": "ok"}