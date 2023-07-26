import time

from celery import shared_task


@shared_task
def long_calculation(x: int, y: int):
    time.sleep(5)
    result = x + y
    return result
