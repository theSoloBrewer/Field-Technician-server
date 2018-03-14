from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
material = Table('material', post_meta,
    Column('m_id', Integer, primary_key=True, nullable=False),
    Column('mat_name', String(length=64)),
    Column('mat_model', String(length=64)),
    Column('mat_manufacture', String(length=64)),
    Column('sn', String(length=64)),
    Column('status', Boolean, nullable=False, default=ColumnDefault(True)),
    Column('type_id', Integer),
    Column('location_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['material'].columns['mat_manufacture'].create()
    post_meta.tables['material'].columns['mat_model'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['material'].columns['mat_manufacture'].drop()
    post_meta.tables['material'].columns['mat_model'].drop()
