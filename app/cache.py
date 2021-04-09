from aioredis import ConnectionsPool
from app.schema import Item
import logging
from typing import Optional


class RedisCaching:
    """Simple object caching"""

    def __init__(self, red: ConnectionsPool, ttl=10, max_use=5):
        self.red = red
        self.ttl = ttl
        self.max_use = max_use

    async def set_cache_item(self, item: Item) -> bool:
        """Set new cached object"""
        await self.red.execute(
            'HSET',
            item.item_id,
            'value',
            item.value,
            'used',
            0
        )
        await self.red.execute(
            'EXPIRE',
            item.item_id,
            self.ttl
        )
        logging.debug(f'Item {item.item_id} cached')
        return True

    async def get_cache_item(self, item_id: int) -> Optional[Item]:
        """Get exist cached object and increase use count"""
        value = await self.red.execute(
            'HGET',
            item_id,
            'value'
        )
        if value is None:
            return False
        used = await self.red.execute(
            'HINCRBY',
            item_id,
            'used',
            1
        )
        if int(used) >= self.max_use:
            await self.drop_cache_item(item_id=item_id)
            logging.debug(f'Max use reached for item {item_id}')
        logging.debug(f'Cache HIT for item {item_id}')
        return Item(id=item_id, value=value)

    async def drop_cache_item(self, item_id: int) -> bool:
        """Drop cache object for any cause"""
        await self.red.execute(
            'DEL',
            item_id
        )
        logging.debug(f'Cache dropped for item {item_id}')
