import logging

from celery import shared_task
from .celery import celery_app

logger = logging.getLogger()


@shared_task
def post_instagram_content(username: str, item: dict):
    logger.info(f"Executing post task for user {username} with item {item}")


@shared_task
def post_instagram_story(username: str, item: dict):
    logger.info(f"Executing story task for user {username} with item {item}")


@celery_app.task
def example_task(data):
    print(f"Received data: {data}")
    return {"message": f"Processed data: {data}"}
