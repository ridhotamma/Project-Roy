from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from app.lifespan import task_runner

from app.routers import (
    user_ig,
    user_ig_post,
    user_ig_schedule,
    user_ig_story,
    instagram,
    proxy,
    auth_user,
)
from app.auth_middleware import auth_middleware

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


# Custom HTTP exception handler
@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"status_code": exc.status_code, "message": exc.detail},
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
app.include_router(auth_user.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(user_ig.router, prefix="/api/v1", tags=["Instagram User"])
app.include_router(user_ig_post.router, prefix="/api/v1", tags=["Instagram Post"])
app.include_router(user_ig_story.router, prefix="/api/v1", tags=["Instagram Story"])
app.include_router(
    user_ig_schedule.router, prefix="/api/v1", tags=["Instagram Upload Schedule"]
)
app.include_router(instagram.router, prefix="/api/v1", tags=["Instagram Upload API"])
app.include_router(proxy.router, prefix="/api/v1", tags=["Proxy"])

# Main entry point
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
