from asyncpgsa import create_pool
from aioredis import create_pool as create_redis
from app.cache import RedisCaching


def setup_events(app, config):
    @app.on_event('startup')
    async def on_startup():
        # Create postgres pool
        app.extra['pg'] = await create_pool(
            dsn=config.get('PG_DSN'),
            min_size=int(config.get('PG_MIN')),
            max_size=int(config.get('PG_MAX'))
        )
        # Create redis pool
        app.extra['red'] = await create_redis(
            config.get('RED_DSN'),
            db=int(config.get('RED_DB')),
            password=config.get('RED_PASSWORD'),
            minsize=int(config.get('RED_MIN')),
            maxsize=int(config.get('RED_MAX'))
        )
        app.extra['cache'] = RedisCaching(red=app.extra['red'])

    @app.on_event('shutdown')
    async def on_shutdown():
        # Close postgres pool
        await app.extra['pg'].close_pool()
        # Close redis pool
        app.extra['red'].close()
        await app.extra['red'].wait_closed()
