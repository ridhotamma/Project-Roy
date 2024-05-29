from celery import shared_task
from .celery import celery_app


@shared_task
def execute_post_task(username: str, item: dict):
    print(f"Executing post task for user {username} with item {item}")
    # Logic to post the content to Instagram


@shared_task
def execute_story_task(username: str, item: dict):
    print(f"Executing story task for user {username} with item {item}")
    # Logic to post the story to Instagram


@celery_app.task
def example_task(data):
    print(f"Received data: {data}")
    return {"message": f"Processed data: {data}"}
