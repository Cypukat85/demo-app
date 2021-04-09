from logging.config import dictConfig
import logging


# Init logger
def get_logger(level):
    dictConfig({
        'version': 1,
        'formatters': {'default': {'format': '[%(asctime)s] %(levelname)s: %(message)s'}},
        'handlers': {
            'stdout': {
                'level': level,
                'class': 'logging.StreamHandler',
                'formatter': 'default'
            }
        },
        'root': {
            'level': level,
            'handlers': ['stdout']
        },
        'loggers': {
            'fastapi': {
                'level': level,
                'handlers': ['stdout'],
                'propagate': False
            },
            'uvicorn': {
                'level': level,
                'handlers': ['stdout'],
                'propagate': False
            }
        },
    })
    return logging
