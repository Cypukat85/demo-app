from asyncpgsa import create_pool


def setup_events(app, config):
    @app.on_event('startup')
    async def on_startup():
        app.extra['pg'] = await create_pool(
            dsn=config.get('PG_DSN'),
            min_size=int(config.get('PG_MIN')),
            max_size=int(config.get('PG_MAX'))
        )

    @app.on_event('shutdown')
    async def on_shutdown():
        await app.extra['pg'].close_pool()
