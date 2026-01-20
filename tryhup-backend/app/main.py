from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.staticfiles import StaticFiles

from app.routers.auth import router as auth_router
from app.routers.users import router as users_router
from app.routers.follows import router as follows_router
from app.routers.likes import router as likes_router
from app.routers.contents import router as contents_router
from app.routers.comments import router as comments_router
from app.routers.admin import router as admin_router
from app.routers.admin_comments import router as admin_comments_router
from app.routers.admin_creators import router as admin_creators_router
from app.routers.meta import router as meta_router


# ===============================
# FASTAPI APP
# ===============================
app = FastAPI(
    title="TryHup API",
    description="Backend TryHup – social video platform",
    version="1.0.0",
)


# ===============================
# CORS
# ===============================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ===============================
# STATIC FILES
# ===============================
app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static",
)


# ===============================
# ROUTERS
# ===============================
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(follows_router)
app.include_router(likes_router)
app.include_router(contents_router)
app.include_router(comments_router)
app.include_router(meta_router)
app.include_router(admin_router)
app.include_router(admin_comments_router)
app.include_router(admin_creators_router)


# ===============================
# SWAGGER JWT CONFIG (NO GLOBAL AUTH)
# ===============================
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    openapi_schema.setdefault("components", {})
    openapi_schema["components"].setdefault("securitySchemes", {})
    openapi_schema["components"]["securitySchemes"]["BearerAuth"] = {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
    }

    # ❌ NESSUNA security globale qui

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


# ===============================
# HEALTH CHECK
# ===============================
@app.get("/", tags=["health"])
def root():
    return {"status": "TryHup backend is running"}
