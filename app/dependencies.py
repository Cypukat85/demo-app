from fastapi import HTTPException, Request, Depends, status
import logging


async def get_postgresql_connection(request: Request):
    """Get postgresql connection"""
    try:
        async with request.app.extra['pg'].acquire() as db:
            yield db
    except Exception as e:
        logging.error(str(e))
        yield None
