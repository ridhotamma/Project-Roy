from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from jose import JWTError

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
)


@app.exception_handler(HTTPException)
async def custom_generatal_error(request: Request, exc: JWTError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"status_code": exc.status_code, "message": exc.detail},
    )


@app.exception_handler(JWTError)
async def custom_jwt_error(request: Request, exc: JWTError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"status_code": exc.status_code, "message": exc.detail},
    )


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"status_code": exc.status_code, "message": exc.detail},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    missing_fields = set()

    for e in exc.errors():
        field = e["loc"][-1]
        message = f"{field.capitalize()} is Required"
        errors.append({"field": field, "message": message})
        missing_fields.add(field)

    formatted_error_message = " and ".join(missing_fields) + " are required"

    return JSONResponse(
        status_code=422,
        content={
            "formatted_error_message": formatted_error_message,
            "detail": errors,
        },
    )


app.middleware("http")(auth_middleware)

app.include_router(auth_user.router, prefix="/auth")
app.include_router(user_ig.router)
app.include_router(user_ig_post.router)
app.include_router(user_ig_story.router)
app.include_router(user_ig_schedule.router)
app.include_router(instagram.router)
app.include_router(proxy.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
