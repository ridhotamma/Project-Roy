from fastapi import FastAPI, Request, status, Depends
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.security import OAuth2PasswordBearer
from starlette.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.lifespan import task_runner
from app.routers import (
    user_ig,
    user_ig_post,
    user_ig_schedule,
    user_ig_story,
    instagram,
    proxy,
    auth_user,
    file_upload,
    gallery,
)
from app.auth_middleware import auth_middleware

# Define the OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

app = FastAPI(
    title="Project Roy",
    description="Content and story social media post automation",
    version="1.0.0",
    contact={
        "name": "Author",
        "email": "ridhotamma@outlook.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "http://www.apache.org/licenses/LICENSE-2.0.html",
    },
    lifespan=task_runner,
)

# CORS setup
origins = [
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Custom HTTP exception handler
@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"status_code": exc.status_code, "message": exc.detail},
    )


# Custom HTTP exception handler
@app.exception_handler(Exception)
async def custom_any_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": str(exc),
        },
    )


# Custom validation exception handler
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    missing_fields = set()

    for error in exc.errors():
        field = error["loc"][-1]
        message = f"{field.capitalize()} is Required"
        errors.append({"field": field, "message": message})
        missing_fields.add(field)

    formatted_error_message = " and ".join(missing_fields) + " are required"

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "formatted_error_message": formatted_error_message,
            "detail": errors,
        },
    )


# Root endpoint
@app.get("/ping")
def read_root():
    return {"message": "Pong"}


# Middleware
app.middleware("http")(auth_middleware)

# Routers
app.include_router(
    auth_user.router,
    prefix="/api/v1/auth",
    tags=["Authentication"],
)
app.include_router(
    user_ig.router,
    prefix="/api/v1",
    tags=["Instagram User"],
    dependencies=[Depends(oauth2_scheme)],
)
app.include_router(
    user_ig_post.router,
    prefix="/api/v1",
    tags=["Instagram Post"],
    dependencies=[Depends(oauth2_scheme)],
)
app.include_router(
    user_ig_story.router,
    prefix="/api/v1",
    tags=["Instagram Story"],
    dependencies=[Depends(oauth2_scheme)],
)
app.include_router(
    user_ig_schedule.router,
    prefix="/api/v1",
    tags=["Instagram Upload Schedule"],
    dependencies=[Depends(oauth2_scheme)],
)
app.include_router(
    instagram.router,
    prefix="/api/v1",
    tags=["Instagram Upload API"],
    dependencies=[Depends(oauth2_scheme)],
)
app.include_router(
    proxy.router,
    prefix="/api/v1",
    tags=["Proxy"],
    dependencies=[Depends(oauth2_scheme)],
)
app.include_router(
    gallery.router,
    prefix="/api/v1",
    tags=["Gallery"],
    dependencies=[Depends(oauth2_scheme)],
)
app.include_router(
    file_upload.router,
    prefix="/api/v1",
    tags=["S3 File upload"],
    dependencies=[Depends(oauth2_scheme)],
)

# Main entry point
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
