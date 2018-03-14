from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
material_contact = Table('material_contact', post_meta,
    Column('material_id', Integer),
    Column('contact_id', Integer),
)

material = Table('material', pre_meta,
    Column('m_id', INTEGER, primary_key=True, nullable=False),
    Column('mat_name', VARCHAR(length=64)),
    Column('sn', VARCHAR(length=64)),
    Column('status', BOOLEAN, nullable=False),
    Column('type_id', INTEGER),
    Column('location_id', INTEGER),
    Column('mat_manufacture', VARCHAR(length=64)),
    Column('mat_model', VARCHAR(length=64)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['material_contact'].create()
    pre_meta.tables['material'].columns['mat_manufacture'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['material_contact'].drop()
    pre_meta.tables['material'].columns['mat_manufacture'].create()
