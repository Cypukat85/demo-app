from os import environ

config = {
    'PG_DSN': environ.get('PG_DSN'),
    'PG_MIN': environ.get('PG_MIN', 1),
    'PG_MAX': environ.get('PG_MAX', 1),
    'RED_DSN': environ.get('RED_DSN'),
    'RED_DB': environ.get('RED_DB', 1),
    'RED_PASSWORD': environ.get('RED_PASSWORD'),
    'RED_MIN': environ.get('RED_MIN', 1),
    'RED_MAX': environ.get('RED_MAX', 1),
    'LOG_LEVEL': environ.get('LOG_LEVEL', 'INFO'),
}
