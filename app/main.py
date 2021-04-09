from fastapi import FastAPI, Depends
from app.config import config
from app.logger import get_logger
from app.events import setup_events
from app.route_api import router as api_router


logger = get_logger(level=config['LOG_LEVEL'])
logger.info(f'Logger level is {config["LOG_LEVEL"]}')
# Create application
app = FastAPI(
    title='Demo app',
    version='v0.1.0'
)

# Application init
setup_events(app=app, config=config)
app.extra.update({'config': config})
# Add routes
app.include_router(
    api_router,
    prefix='/api',
    tags=['DEMO API']
)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
