from sqlalchemy import create_engine, orm

from libs import paths

engine = create_engine(paths.DB_CONN_STR, echo=False)
mapper_registry = orm.registry()
Base = mapper_registry.generate_base()