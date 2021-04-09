import sqlalchemy as sa
from sqlalchemy import PrimaryKeyConstraint, ForeignKeyConstraint, UniqueConstraint, ForeignKey

meta = sa.MetaData()


items = sa.Table(
    'items', meta,
    sa.Column('id', sa.INT),
    sa.Column('value', sa.VARCHAR, nullable=True),
    PrimaryKeyConstraint('id', name='pk_items')
)
