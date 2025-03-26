from contextlib import asynccontextmanager
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from .auth.router import auth_router
from .database import connect_mongodb, disconnect_mongodb, initialize_supabase
from .config import settings

# Lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Any startup initialization
    await initialize_supabase()
    connect_mongodb()
    yield
    # Any actions needed on shutdown
    disconnect_mongodb()

# FastAPI App Initialization
async def not_found(request, exc):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": [{"msg": "API Route not found."}]}
    )

exception_handlers = {404: not_found}
app = FastAPI(
  title="Academic Weapon API",
  version="1.0",
  exception_handlers=exception_handlers,
  openapi_url="/openapi.json",
  lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=settings.CORS_HEADERS,
)

# Routes
@app.get("/")
async def root():
    return {"message": "hello world"}

@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify API is running.
    """
    return {"status": "healthy"}

app.include_router(
    auth_router,
    prefix="/auth",
    tags=["Authentication"]
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)