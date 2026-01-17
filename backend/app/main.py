from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from contextlib import asynccontextmanager
from app.config import settings
from app.api.v1.router import api_router
from app. services.items_database_manager import items_db_manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle events"""
    # Startup:  Initialize items database
    print("🚀 Starting SC-AUC-Monitoring...")
    await items_db_manager.initialize()
    print("✅ Application ready!")
    
    yield
    
    # Shutdown
    print("👋 Shutting down...")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan,  # ← Добавить lifecycle
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
frontend_static = Path(__file__).parent.parent. parent / "frontend" / "static"
if frontend_static.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_static)), name="static")

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return RedirectResponse(url="/static/favicon.ico")


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
        "items_db_last_update": items_db_manager.last_update.isoformat() if items_db_manager.last_update else None,
        "items_db_total": sum(len(items) for items in items_db_manager.search_index.values()),
    }