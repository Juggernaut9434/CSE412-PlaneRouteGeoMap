from tkinter import EXCEPTION
import psycopg2
from config import config
from route import Route
# psycopg2 Documentation: https://www.psycopg.org/docs/index.html

class Database():
	conn = None
	cursor = None
	routes: list[Route] = []
	"""Contains list of ALL routes possible.
	For filtering: Run SQL and find airport_id's that matter and check if they match for src_id and/or dest_id as needed"""

	def __init__(self, printSQL=True) -> None:
		self.printSQL = printSQL
		"""Creates a connection to database with configuration specified in database.ini"""
		try:
			# Connect to database and create cursor
			self.conn: psycopg2.connection = psycopg2.connect(**config())
			self.cursor = self.conn.cursor()

			# Test connection by printing PostgreSQL version
			print("Connected to database.\nPostgreSQL version:", end=' ')
			self.cursor.execute("SELECT version()")
			print(self.cursor.fetchone()[0], end='\n\n')
			self.loadRoutes()

			# Test getRoutesFromCity function
			x = self.getRoutesFromCity("Baltimore")
			for route in x:
				print(route.airline + "\tFLIES ROUTE:\t" + route.src_iata + " -> " + route.dest_iata)

		except (Exception, psycopg2.DatabaseError) as error:
			print(error)
			self.closeConnection()

# TODO: SURROUND ALL METHODS WITH TRY AND CATCH ERRORS AND CLOSE CONNECTION LIKE ABOVE IN INIT
# NOT SURE IF CLOSING CONNECTION REALLY MATTERS BUT WE TRYING TO BE GOOD PROGRAMMERS HERE RIGHT?

	def loadRoutes(self):
		"""Loads ALL possible routes into self.routes"""
		sql = f"SELECT airline, src_airport, dest_airport FROM route"
		self.logSQL(sql)
		self.cursor.execute(sql)
		ALLroutes = self.cursor.fetchall()
		
		for route in ALLroutes:
			airline, srcIata, destIata = route
			srcAirport = self.getAirportLatLongFromIata(srcIata)
			destAirport = self.getAirportLatLongFromIata(destIata)


			if srcAirport is not None and destAirport is not None:
				srcLat, srcLong = srcAirport[0], srcAirport[1]
				destLat, destLong = destAirport[0], destAirport[1]

			if airline is not None and srcLat is not None and srcLong is not None and destLat is not None and destLong is not None:
				# If all of the values have been iniatialized, add route in self.routes
				self.routes.append(Route(airline, srcIata, srcLat, srcLong, destIata, destLat, destLong))
				
	# Don't double ask for airports that are used multiple times (use a dictionary mapping IATA -> Tuple(lat, long))
	loadedAirports: dict[str, tuple] = {}

	def getAirportLatLongFromIata(self, iata: int):
		if iata is None:
			self.warning("Airport requested with no IATA, returning (None, None) for lat/long")
			return (None, None)
		elif self.loadedAirports.get(iata) is not None:
			return self.loadedAirports.get(iata)
		else:
			sql = f"SELECT latitude, longitude FROM airport WHERE iata='{iata}'"
			self.logSQL(sql)
			# Adding airport. and route. to make the SQL execute faster
			sql = f"SELECT latitude, longitude FROM airport WHERE airport.iata='{iata}'"
			self.cursor.execute(sql)
			self.loadedAirports[iata] = self.cursor.fetchone()
			return self.loadedAirports[iata]
			
	def findRoute(self, airline: str, src_iata: int, dest_iata: int) -> Route:
		"""Filters ALL routes by airline, source airport IATA and destination airport IATA to find a specific route in self.routes
		NOTE: IATA is used instead of ID throughout this code once I realized all routes in the database had an IATA src and dest but some ids were NULL"""
		foundRoute: Route = None
		
		for route in self.routes:
			if route.airline == airline and route.src_iata == src_iata and route.dest_iata == dest_iata:
				foundRoute = route
		
		if foundRoute is None:
			self.warning("No route found from " + src_iata + " to " + dest_iata)

		# Could be reduced to one line using a Python generator but they make things kinda hard to understand code imo:
		# return (r for r in self.routes if r.airline == airline and r.src_iata == src_iata and r.dest_iata == dest_iata).__next__()
		return foundRoute

	def getRoutesFromCity(self, city: str) -> list[Route]:
		"""Find routes leaving from some city"""
		sql = f"SELECT airline, src_airport, dest_airport FROM route, airport WHERE city ILIKE '{city}' AND src_airport=iata"
		self.logSQL(sql)
		# Adding airport. and route. to make the SQL execute faster
		sql = f"SELECT airline, src_airport, dest_airport FROM route, airport WHERE airport.city ILIKE '{city}' AND route.src_airport=airport.iata"
		self.cursor.execute(sql)
		filteredRoutes: list[Route] = []

		for route in self.cursor.fetchall():
			if route is None:
				self.warning(f"No routes found in getRoutesFromCity({city})")
			else:
				filteredRoutes.append(self.findRoute(route[0], route[1], route[2]))
		
		return filteredRoutes
				
	def closeConnection(self):
		if self.conn is not None and not self.conn.closed:
			self.conn.close()
			print("Database connection closed.")

	def logSQL(self, SQL: str):
		if self.printSQL:
			print("Executing '" + SQL + "'")

	def warning(self, warning: str):
		print("WARNING: " + warning)

if __name__ == '__main__':
	db = Database()