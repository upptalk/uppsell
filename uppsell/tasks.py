from __future__ import absolute_import
from celery import shared_task

@shared_task
def add(x, y):
    return x + y

@shared_task
def mul(x, y):
    return x * y

from time import sleep

@shared_task
def xsum(numbers):
    sleep(10)
    return sum(numbers)

