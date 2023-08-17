from connection.create_engine import connect_to_engine
from models.models import Base
import models.base_reports as br

engine = connect_to_engine("/home/balch027/dbr/dbr/chinook.db")
metadata = Base.metadata
br.metadata_report(metadata)