import os
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from progressbar import Percentage, ProgressBar, RotatingMarker, Bar, ETA

from api import ApiClient
from models import Agency, Route, Stop

def main():
	## Pull PostgreSQL information from the environment
	pg_passwd = os.environ['POSTGRES_ENV_POSTGRES_PASSWORD']
	pg_port = os.environ['POSTGRES_PORT_5432_TCP_PORT']
	pg_addr = os.environ['POSTGRES_PORT_5432_TCP_ADDR']
	pg_dn = 'postgresql://postgres:%s@%s:%s/postgres' % (pg_passwd, pg_addr, pg_port)

	## Create the sqlalchemy session
	engine = create_engine(pg_dn)
	Session = sessionmaker()
	Session.configure(bind=engine)
	session = Session()

	## Flushing after every bulk_save_objects for sake of sanity with debugging
	## and unpredictable timing

	## Using bulk_save_objects instead of add_all for sake of duplicate primary keys
	## merge could also be used in this case

	## Truncate tables each run (this order necessary for foreign key constraints)
	sys.stdout.write('Truncating Tables\n')
	sys.stdout.flush()
	session.query(Stop).delete()
	session.query(Route).delete()
	session.query(Agency).delete()

	## Load all the agencies from the api and create model objects for them
	sys.stdout.write('Loading Agencies\n')
	sys.stdout.flush()
	agencies = ApiClient.get_agencies()
	session.bulk_save_objects(agencies)
	session.flush()

	progress_widgets = ['Saving: ', Percentage(), ' ', Bar(marker=RotatingMarker()), ' ', ETA()]

	## For each of the agencies loaded, gather the routes
	sys.stdout.write('Loading routes for all agencies\n')
	sys.stdout.flush()
	pbar = ProgressBar(term_width=50, widgets=progress_widgets)
	for a in pbar(agencies):
		for r in ApiClient.get_routes(a.id):
			session.merge(r)
		session.flush()

	sys.stdout.write('\n')
	sys.stdout.flush()

	## For each of the agencies loaded, gather the stops
	sys.stdout.write('Loading stops for all agencies\n')
	sys.stdout.flush()
	pbar = ProgressBar(term_width=50, widgets=progress_widgets)
	for a in pbar(agencies):
		for s in ApiClient.get_stops(a.id):
			session.merge(s)
		session.flush()

if __name__ == "__main__":
    main()
