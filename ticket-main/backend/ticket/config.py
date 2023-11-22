
SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authentication-Token'
SECURITY_PASSWORD_SALT = 'SALT'
SECURITY_PASSWORD_HASH = 'bcrypt'
WTF_CSRF_ENABLED = False
JWT_SECRET_KEY = 'JWT_SECRET_KEY'

CSV_EXPORT_PATH = '/path/to/csv/exports/directory'


EMAIL_TEMPLATES = 'templates/'
# EXPORT_FOLDER = 'backend/templates/CSV exports/'
# PDF_TEMPLATES = 'backend/templates/'


CACHE_TYPE = "redis"
CACHE_REDIS_URL = "redis://localhost:6379/0"
CACHE_DEFAULT_TIMEOUT = 300
DEBUG = False


CELERY_broker_url = "redis://localhost:6379/1"
CELERY_RESULT_BACKEND = "redis://localhost:6379/2"
CELERY_broker_connection_retry_on_startup=True
CELERY_timezone = "Asia/Kolkata"