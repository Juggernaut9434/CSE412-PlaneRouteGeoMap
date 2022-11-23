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

		except (Exception, psycopg2.DatabaseError) as error:
			self.closeConnection(error)

# TODO: SURROUND ALL METHODS WITH TRY AND CATCH ERRORS AND CLOSE CONNECTION LIKE ABOVE IN INIT
# NOT SURE IF CLOSING CONNECTION REALLY MATTERS BUT WE TRYING TO BE GOOD PROGRAMMERS HERE RIGHT?

# ALSO SHOULD ADD A FUNCTION TO GET AIRPORT NAME AND CITY NAME FROM AIRPORT IATA MAYBE?

	def loadRoutes(self):
		"""Loads ALL possible routes into self.routes"""
		try:
			sql = f"SELECT airline, src.iata, src.latitude, src.longitude, dest.iata, dest.latitude, dest.longitude \n\t\
					FROM route r \n\t\
					INNER JOIN airport as src ON src.iata = r.src_airport \n\t\
					INNER JOIN airport as dest ON dest.iata = r.dest_airport"
			self.logSQL(sql)
			self.cursor.execute(sql)
			ALLroutes = self.cursor.fetchall()
		except (Exception, psycopg2.DatabaseError) as error:
			self.closeConnection(error)
			return
		
		for route in ALLroutes:
			if route is None:
				self.warning("No routes found in attempt to find all routes - Please check database connection")
				continue # I'm pretty sure it should only be None is no routes at all are found but continue instead of break just in case there are routes
			airline, srcIata, srcLat, srcLong, destIata, destLat, destLong = route

			if airline is not None and \
				srcIata is not None and srcLat is not None and srcLong is not None and \
				destIata is not None and destLat is not None and destLong is not None:
				# If all of the values have been iniatialized, add route in self.routes
				self.routes.append(Route(airline, srcIata, srcLat, srcLong, destIata, destLat, destLong))
			else:
				self.warning("Failure in attempted route (missing values):", Route(airline, srcIata, srcLat, srcLong, destIata, destLat, destLong))
			
	def findRoute(self, airline: str, src_iata: int, dest_iata: int) -> Route:
		"""Filters ALL routes by airline, source airport IATA and destination airport IATA to find a specific route in self.routes"""
		foundRoute: Route = None
		
		# Could be reduced to one line using a Python generator but they make things kinda hard to understand code imo:
		# foundRoute =  (r for r in self.routes if r.airline == airline and r.src_iata == src_iata and r.dest_iata == dest_iata).__next__()
		for route in self.routes:
			if route.airline == airline and route.src_iata == src_iata and route.dest_iata == dest_iata:
				foundRoute = route
		
		if foundRoute is None:
			self.warning(f"No route found from {src_iata} to {dest_iata}, returning None")

		return foundRoute

# Routes From Location Functions

	def getRoutesFromCity(self, city: str) -> list[Route]:
		"""Find routes leaving from some city"""
		try:
			sql = f"SELECT airline, src_airport, dest_airport FROM route, airport WHERE city ILIKE '{city}' AND src_airport=iata"
			self.logSQL(sql)
			# Adding airport. and route. to make the SQL execute faster
			sql = f"SELECT airline, src_airport, dest_airport FROM route, airport WHERE airport.city ILIKE '{city}' AND route.src_airport=airport.iata"
			self.cursor.execute(sql)
		except (Exception, psycopg2.DatabaseError) as error:
			self.closeConnection(error)

		return self.getRouteListFromCursor(warningMessage = f"No routes found in getRoutesFromCity({city})")
			
	def getRoutesFromIata(self, iata: str) -> list[Route]:
		"""Find routes leaving from some airport"""
		try:
			iata = iata.upper()
			sql = f"SELECT airline, src_airport, dest_airport FROM route WHERE src_airport='{iata}'"
			self.logSQL(sql)
			# Adding airport. and route. to make the SQL execute faster
			sql = f"SELECT airline, src_airport, dest_airport FROM route WHERE route.src_airport='{iata}'"
			self.cursor.execute(sql)
		except (Exception, psycopg2.DatabaseError) as error:
			self.closeConnection(error)

		return self.getRouteListFromCursor(warningMessage = f"No routes found in getRoutesFromIata({iata})")
					
# Routes To Location Functions

	def getRoutesToCity(self, city: str) -> list[Route]:
		"""Find routes leaving from some city"""
		try:
			sql = f"SELECT airline, src_airport, dest_airport FROM route, airport WHERE city ILIKE '{city}' AND dest_airport=iata"
			self.logSQL(sql)
			self.cursor.execute(sql)
			return self.getRouteListFromCursor(warningMessage = f"No routes found in getRoutesToCity({city})")
		except (Exception, psycopg2.DatabaseError) as error:
			self.closeConnection(error)
			
	def getRoutesToIata(self, iata: str) -> list[Route]:
		"""Find routes leaving from some airport"""
		try:
			iata = iata.upper()
			sql = f"SELECT airline, src_airport, dest_airport FROM route WHERE dest_airport='{iata}'"
			self.logSQL(sql)
			self.cursor.execute(sql)
			return self.getRouteListFromCursor(warningMessage = f"No routes found in getRoutesToIata({iata})")
		except (Exception, psycopg2.DatabaseError) as error:
			self.closeConnection(error)

	def getRouteListFromCursor(self, warningMessage: str = None) -> list[Route]:
		"""Creates and returns a list of Routes from all routes (airline, src_airport, dest_airport) currently in cursor"""
		routesInCursor: list[Route] = []

		for route in self.cursor.fetchall():
			if route is None and warningMessage is not None:
				self.warning(warningMessage)
			else:
				routesInCursor.append(self.findRoute(route[0], route[1], route[2]))

		return routesInCursor

	def closeConnection(self, message = None):
		if message is not None:
			print("\n" + message)
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

	# Test getRoutesFromCity and getRoutesFromIata functions
	x = db.getRoutesFromCity("Baltimore")
	for route in x:
		print(str(route))

	x = db.getRoutesFromIata("BOS")
	for route in x:
		print(str(route))

	db.closeConnection("Database testing completed.")