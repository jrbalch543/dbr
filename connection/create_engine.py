import sqlalchemy as sql

from models.models import Base

class Engine():
    def __init__(self, db_path, db_type="sqlite", existing_models=None) -> None:
        self.db_path = db_path
        self.db_type = db_type
        self.existing_models = existing_models
        self._base = Base
        self.connect_to_engine()
        

    def connect_to_engine(self):
        if self.db_type == "sqlite":
            self._engine = sql.create_engine(f"sqlite:///{self.db_path}")
            self._base.prepare(autoload_with = self._engine, reflect=True)