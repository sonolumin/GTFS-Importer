from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Text, Float, ForeignKey
from geoalchemy2 import Geometry

Base = declarative_base()

class Agency(Base):
	__tablename__ = 'gtfs_agency'
	id = Column('agency_id', Text, primary_key=True)
	name = Column('agency_name', Text)
	url = Column('agency_url', Text)
	timezone = Column('agency_timezone', Text, default='')
	routes = relationship("Route")

class Route(Base):
	__tablename__ = 'gtfs_routes'
	id = Column('route_id', Text, primary_key=True)
	agency_id = Column('agency_id', Text, ForeignKey('gtfs_agency.agency_id'))
	short_name = Column('route_short_name', Text)
	long_name = Column('route_long_name', Text)
	color = Column('route_color', Text)

class Stop(Base):
	__tablename__ = 'gtfs_stops'
	id = Column('stop_id', Text, primary_key=True)
	name = Column('stop_name', Text)
	code = Column('stop_code', Text)
	lat = Column('stop_lat', Float)
	lon = Column('stop_lon', Float)
	geom = Column('the_geom', Geometry('POINT', 900913))