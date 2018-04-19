from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
address = Table('address', post_meta,
    Column('a_id', Integer, primary_key=True, nullable=False),
    Column('street', String(length=128), nullable=False),
    Column('city', String(length=128), nullable=False),
    Column('state', String(length=64), nullable=False),
)

contact_info = Table('contact_info', post_meta,
    Column('c_id', Integer, primary_key=True, nullable=False),
    Column('contact_name', String(length=64), nullable=False),
    Column('email', String(length=128)),
    Column('phone', Integer),
    Column('addr_id', Integer),
    Column('c_type_id', Integer),
)

labor = Table('labor', post_meta,
    Column('l_id', Integer, primary_key=True, nullable=False),
    Column('task', Text),
    Column('user_id', Integer),
)

labor_project = Table('labor_project', post_meta,
    Column('project_id', Integer),
    Column('labor_id', Integer),
)

material = Table('material', post_meta,
    Column('m_id', Integer, primary_key=True, nullable=False),
    Column('mat_name', String(length=64)),
    Column('mat_model', String(length=64)),
    Column('sn', String(length=64)),
    Column('status', Boolean, nullable=False, default=ColumnDefault(True)),
    Column('type_id', Integer),
    Column('location_id', Integer),
)

material_contact = Table('material_contact', post_meta,
    Column('material_id', Integer),
    Column('contact_id', Integer),
)

material_location = Table('material_location', post_meta,
    Column('ml_id', Integer, primary_key=True, nullable=False),
    Column('ml_name', String(length=64)),
    Column('type_id', Integer),
)

material_project = Table('material_project', post_meta,
    Column('project_id', Integer),
    Column('material_id', Integer),
)

project = Table('project', post_meta,
    Column('p_id', Integer, primary_key=True, nullable=False),
    Column('pro_name', String(length=64), nullable=False),
    Column('code', String(length=6), nullable=False),
    Column('description', Text),
    Column('status_id', Integer),
    Column('location_id', Integer),
    Column('poc_id', Integer),
)

type = Table('type', post_meta,
    Column('t_id', Integer, primary_key=True, nullable=False),
    Column('type_name', String(length=64)),
)

user = Table('user', post_meta,
    Column('u_id', Integer, primary_key=True, nullable=False),
    Column('username', String(length=128), nullable=False),
    Column('password', String(length=256)),
    Column('type_id', Integer),
    Column('contact_id', Integer),
    Column('address_id', Integer),
)

user_project = Table('user_project', post_meta,
    Column('project_id', Integer),
    Column('user_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['address'].create()
    post_meta.tables['contact_info'].create()
    post_meta.tables['labor'].create()
    post_meta.tables['labor_project'].create()
    post_meta.tables['material'].create()
    post_meta.tables['material_contact'].create()
    post_meta.tables['material_location'].create()
    post_meta.tables['material_project'].create()
    post_meta.tables['project'].create()
    post_meta.tables['type'].create()
    post_meta.tables['user'].create()
    post_meta.tables['user_project'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['address'].drop()
    post_meta.tables['contact_info'].drop()
    post_meta.tables['labor'].drop()
    post_meta.tables['labor_project'].drop()
    post_meta.tables['material'].drop()
    post_meta.tables['material_contact'].drop()
    post_meta.tables['material_location'].drop()
    post_meta.tables['material_project'].drop()
    post_meta.tables['project'].drop()
    post_meta.tables['type'].drop()
    post_meta.tables['user'].drop()
    post_meta.tables['user_project'].drop()
