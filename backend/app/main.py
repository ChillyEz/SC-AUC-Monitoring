from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from app.config import settings
from app.api.v1.router import api_router

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Routes
app.include_router(api_router, prefix=settings.API_V1_PREFIX)

# Static files (frontend)
frontend_static = Path(__file__).parent.parent.parent / "frontend" / "static"
if frontend_static.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_static)), name="static")


# Serve index.html
@app.get("/", response_class=HTMLResponse)
async def root():
    frontend_index = (
        Path(__file__).parent.parent.parent / "frontend" / "templates" / "index.html"
    )
    if frontend_index.exists():
        return frontend_index.read_text(encoding="utf-8")
    return "<h1>SC-AUC-Monitoring</h1><p>Frontend not found</p>"


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "version": settings.APP_VERSION,
        "environment": settings.ENV,
        "api_source": settings.API_SOURCE,
        "using_demo_api": settings.API_SOURCE == "demo",
    }
