from os import environ

config = {
    'PG_DSN': environ.get('PG_DSN'),
    'PG_MIN': environ.get('PG_MIN', 1),
    'PG_MAX': environ.get('PG_MAX', 1),
    'LOG_LEVEL': environ.get('LOG_LEVEL', 'INFO'),
}
