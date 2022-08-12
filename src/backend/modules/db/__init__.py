import os
from sqlalchemy import create_engine, orm

from libs import paths, utils

utils.load_env()


def get_db_conn_str():
    driver = os.getenv('DB_CONNECTION')
    host = os.getenv('DB_HOST')
    port = os.getenv('DB_PORT')
    dbname = os.getenv('DB_DATABASE')
    username = os.getenv('DB_USERNAME')
    password = os.getenv('DB_PASSWORD')

    if driver == 'sqlite':
        return f"sqlite:///{str(paths.STORAGE_DIR)}/{dbname}"

    return f"{driver}://{username}:{password}@{host}:{port}/{dbname}"


engine = create_engine(get_db_conn_str(), echo=False)
mapper_registry = orm.registry()
Base = mapper_registry.generate_base()