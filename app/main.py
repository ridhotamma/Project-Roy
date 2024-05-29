from fastapi import FastAPI
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

app.middleware("http")(auth_middleware)

app.include_router(user_ig.router)
app.include_router(user_ig_post.router)
app.include_router(user_ig_story.router)
app.include_router(user_ig_schedule.router)
app.include_router(instagram.router)
app.include_router(proxy.router)
app.include_router(auth_user.router, prefix="/auth")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
