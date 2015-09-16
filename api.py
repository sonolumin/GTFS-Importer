import urllib2
import json
from models import Agency, Route, Stop

class ApiClient:
	base_url = "http://api.availabs.org/gtfs/"

	@staticmethod
	def get_agencies():
		f = urllib2.urlopen(ApiClient.base_url + "agency/")
		agencies_base = json.load(f)
		agencies = []
		for a in agencies_base:
			agencies.append(Agency(
				id=str(a['id']),
				name=a['name'],
				url=a['url']
			))
		return agencies

	@staticmethod
	def get_routes(agency_id):
		f = urllib2.urlopen(ApiClient.base_url + "agency/" + str(agency_id) + "/routes?format=geo")
		routes_base = json.load(f)
		routes = []
		for r in routes_base['features']:
			props = r['properties']
			routes.append(Route(
				id=str(props['route_id']),
				agency_id=agency_id,
				short_name=props['route_short_name'],
				long_name=props['route_long_name'],
				color=props['route_color']
			))

		return routes

	@staticmethod
	def get_stops(agency_id):
		f = urllib2.urlopen(ApiClient.base_url + "agency/" + str(agency_id) + "/stops?format=geo")
		stops_base = json.load(f)
		stops = []
		for r in stops_base['features']:
			props = r['properties']
			geo = r['geometry']

			[lon, lat] = geo['coordinates']

			stops.append(Stop(
				id=str(props['stop_id']),
				name=props['stop_name'],
				code=props['stop_code'],
				lat=lat,
				lon=lon,
				geom=('SRID=900913;POINT(%f %f)' % (lon, lat))
			))

		return stops

