from fastapi import FastAPI
from app.routers import user_ig, user_ig_post, user_ig_schedule, user_ig_story, instagram, proxy

app = FastAPI()

app.include_router(user_ig.router)
app.include_router(user_ig_post.router)
app.include_router(user_ig_story.router)
app.include_router(user_ig_schedule.router)
app.include_router(instagram.router)
app.include_router(proxy.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
