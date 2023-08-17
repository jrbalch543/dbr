import sqlalchemy as sql

from models.models import Base

def connect_to_engine(db_path, db_type="sqlite", existing_models=None):
    if db_type == "sqlite":
        engine = sql.create_engine(f"sqlite:///{db_path}")
        Base.prepare(autoload_with = engine, reflect=True)
        return engine