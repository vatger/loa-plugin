import json

import requests

from core.celery import celery_app
from core.redis import redis_app


@celery_app.task(name="tasks.datafeed.update_datafeed")
def update_datafeed():
    data = requests.get("https://data.vatsim.net/v3/vatsim-data.json").json()
    redis_app.set("datafeed", json.dumps(data))
