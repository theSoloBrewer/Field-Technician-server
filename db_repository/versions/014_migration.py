from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
project = Table('project', pre_meta,
    Column('p_id', INTEGER, primary_key=True, nullable=False),
    Column('pro_name', VARCHAR(length=64), nullable=False),
    Column('code', VARCHAR(length=6), nullable=False),
    Column('description', TEXT),
    Column('location_id', INTEGER),
    Column('poc_id', INTEGER),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['project'].columns['poc_id'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['project'].columns['poc_id'].create()
