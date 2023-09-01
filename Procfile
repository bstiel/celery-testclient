web: python main.py
celery: watchfiles --filter python 'celery --app worker.app worker --pool prefork --concurrency 1 --loglevel INFO' .