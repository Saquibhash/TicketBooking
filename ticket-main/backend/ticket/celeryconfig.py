broker_url = "redis://localhost:6379/1"
RESULT_BACKEND = "redis://localhost:6379/2"

broker_connection_retry_on_startup = True
timezone = "Asia/Kolkata"

RESULT_BACKEND_TRANSPORT_OPTIONS = {
    'visibility_timeout': 3600,
    'fanout_patterns': True,
    'fanout_prefix': True,
    'max_connections': 10,
}

RESULT_SERIALIZER = "json"
TASK_RESULT_EXPIRES = 3600
RESULT_PERSISTENT = True


# celery upgrade settings /home/saquibeckham/Desktop/celery\ test/cel/celeryconfig.py

# client pushes the msg in msg broker --> celery distributes the task to the workers ___>
# Once the task is complete the result will be pushed to the backend
