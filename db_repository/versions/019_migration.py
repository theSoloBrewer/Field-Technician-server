from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
contact_info = Table('contact_info', post_meta,
    Column('c_id', Integer, primary_key=True, nullable=False),
    Column('contact_name', String(length=64), nullable=False),
    Column('email', String(length=128)),
    Column('phone', Integer),
    Column('addr_id', Integer),
    Column('c_type_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['contact_info'].columns['addr_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['contact_info'].columns['addr_id'].drop()
