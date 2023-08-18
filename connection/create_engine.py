import sqlalchemy as sql

from models.models import Base

class Engine():
    def __init__(self, db_path, db_type="sqlite") -> None:
        self.db_path = db_path
        self.db_type = db_type
        self._base = Base
        self.connect_to_engine()
        

    def connect_to_engine(self):
        if self.db_type == "sqlite":
            self._engine = sql.create_engine(f"sqlite:///{self.db_path}")
            self._base.prepare(autoload_with = self._engine, reflect=True)