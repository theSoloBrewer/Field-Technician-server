from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
address = Table('address', pre_meta,
    Column('a_id', INTEGER, primary_key=True, nullable=False),
    Column('street', VARCHAR(length=128), nullable=False),
    Column('city', VARCHAR(length=128), nullable=False),
    Column('state', VARCHAR(length=64), nullable=False),
)

contact_info = Table('contact_info', pre_meta,
    Column('c_id', INTEGER, primary_key=True, nullable=False),
    Column('contact_name', VARCHAR(length=64), nullable=False),
    Column('email', VARCHAR(length=128)),
    Column('phone', INTEGER),
    Column('c_type_id', INTEGER),
    Column('addr_id', INTEGER),
)

labor = Table('labor', pre_meta,
    Column('l_id', INTEGER, primary_key=True, nullable=False),
    Column('task', TEXT),
    Column('user_id', INTEGER),
)

labor_project = Table('labor_project', pre_meta,
    Column('project_id', INTEGER),
    Column('labor_id', INTEGER),
)

material = Table('material', pre_meta,
    Column('m_id', INTEGER, primary_key=True, nullable=False),
    Column('mat_name', VARCHAR(length=64)),
    Column('sn', VARCHAR(length=64)),
    Column('status', BOOLEAN, nullable=False),
    Column('type_id', INTEGER),
    Column('location_id', INTEGER),
    Column('mat_model', VARCHAR(length=64)),
)

material_contact = Table('material_contact', pre_meta,
    Column('material_id', INTEGER),
    Column('contact_id', INTEGER),
)

material_location = Table('material_location', pre_meta,
    Column('ml_id', INTEGER, primary_key=True, nullable=False),
    Column('ml_name', VARCHAR(length=64)),
    Column('type_id', INTEGER),
)

material_project = Table('material_project', pre_meta,
    Column('project_id', INTEGER),
    Column('material_id', INTEGER),
)

project = Table('project', pre_meta,
    Column('p_id', INTEGER, primary_key=True, nullable=False),
    Column('pro_name', VARCHAR(length=64), nullable=False),
    Column('code', VARCHAR(length=6), nullable=False),
    Column('description', TEXT),
    Column('location_id', INTEGER),
    Column('poc_id', INTEGER),
    Column('status_id', INTEGER),
)

type = Table('type', pre_meta,
    Column('t_id', INTEGER, primary_key=True, nullable=False),
    Column('type_name', VARCHAR(length=64)),
)

user = Table('user', pre_meta,
    Column('u_id', INTEGER, primary_key=True, nullable=False),
    Column('username', VARCHAR(length=128), nullable=False),
    Column('type_id', INTEGER),
    Column('contact_id', INTEGER),
    Column('address_id', INTEGER),
    Column('password', VARCHAR(length=256)),
)

user_project = Table('user_project', pre_meta,
    Column('project_id', INTEGER),
    Column('user_id', INTEGER),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['address'].drop()
    pre_meta.tables['contact_info'].drop()
    pre_meta.tables['labor'].drop()
    pre_meta.tables['labor_project'].drop()
    pre_meta.tables['material'].drop()
    pre_meta.tables['material_contact'].drop()
    pre_meta.tables['material_location'].drop()
    pre_meta.tables['material_project'].drop()
    pre_meta.tables['project'].drop()
    pre_meta.tables['type'].drop()
    pre_meta.tables['user'].drop()
    pre_meta.tables['user_project'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['address'].create()
    pre_meta.tables['contact_info'].create()
    pre_meta.tables['labor'].create()
    pre_meta.tables['labor_project'].create()
    pre_meta.tables['material'].create()
    pre_meta.tables['material_contact'].create()
    pre_meta.tables['material_location'].create()
    pre_meta.tables['material_project'].create()
    pre_meta.tables['project'].create()
    pre_meta.tables['type'].create()
    pre_meta.tables['user'].create()
    pre_meta.tables['user_project'].create()
