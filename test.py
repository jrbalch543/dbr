from connection.create_engine import Engine
from run.parse_args import parse
from tasks.tasks import Dbr, run_cli_loop

args = parse()
engine = Engine(args.db_path)
run_cli_loop(engine)
# print(engine._base.metadata.tables['albums'].__dict__['_columns'])
