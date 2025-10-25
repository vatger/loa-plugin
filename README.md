# loa-plugin

uv run celery -A core.celery.celery_app beat --loglevel=info  
uv run celery -A core.celery.celery_app worker --loglevel=info