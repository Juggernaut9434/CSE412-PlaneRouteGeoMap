from tkinter import EXCEPTION
import psycopg2
from .config import config
from .route import Route
# psycopg2 Documentation: https://www.psycopg.org/docs/index.html

class Database():
	conn = None
	cursor = None
	routes: list[Route] = []
	"""Contains list of ALL routes possible.
	For filtering: Run SQL and find airport_id's that matter and check if they match for src_id and/or dest_id as needed"""

	def __init__(self, maxRoutes: int, printSQL=True) -> None:
		self.printSQL = printSQL
		"""Creates a connection to database with configuration specified in database.ini"""
		try:
			# Connect to database and create cursor
			dbConfig = config()

			if len(dbConfig) < 5:
				self.warning("Unable to load database configuration.")
			
			self.conn: psycopg2.connection = psycopg2.connect(**dbConfig)
			self.cursor = self.conn.cursor()

			# Test connection by printing PostgreSQL version
			print("LOG: Connected to database.\nPostgreSQL version:", end=' ')
			self.cursor.execute("SELECT version()")
			print("LOG: " + self.cursor.fetchone()[0], end='\n\n')
			# self.loadRoutes(maxRoutes)

		except (Exception, psycopg2.DatabaseError) as error:
			self.closeConnection(error)

# NOT SURE IF CLOSING CONNECTION REALLY MATTERS BUT WE TRYING TO BE GOOD PROGRAMMERS HERE RIGHT?

# ALSO SHOULD ADD A FUNCTION TO GET AIRPORT NAME AND CITY NAME FROM AIRPORT IATA MAYBE?

	def loadRoutes(self, randomSampleSize):
		"""Loads ALL possible routes into self.routes"""
		try:
			sql = f"""SELECT * FROM routes_coor \n
                    WHERE src_country = 'United States'	\n
					ORDER BY random() LIMIT {randomSampleSize}"""
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
			airline, srcIata, srcLat, srcLong, destIata, destLat, destLong, _, _, _, _ = route

			if airline is not None and \
				srcIata is not None and srcLat is not None and srcLong is not None and \
				destIata is not None and destLat is not None and destLong is not None:
				# If all of the values have been iniatialized, add route in self.routes
				self.routes.append(Route(airline, srcIata, srcLat, srcLong, destIata, destLat, destLong))
			else:
				self.warning("Failure in attempted route (missing values):", 
                    Route(airline, srcIata, srcLat, srcLong, destIata, destLat, destLong))

# Routes From Location Functions
	def getRoutesAll(self) -> list[Route]:
		self.loadRoutes(1000)
		return self.routes

	def getRoutesFromCity(self, city: str) -> list[Route]:
		"""Find routes leaving from some city"""
		try:
			sql = f"""SELECT * FROM routes_coor
                    WHERE src_city ILIKE '{city}'"""
			self.logSQL(sql)
			self.cursor.execute(sql)
		except (Exception, psycopg2.DatabaseError) as error:
			self.closeConnection(error)

		return self.getRouteListFromCursor(warningMessage = f"No routes found in getRoutesFromCity({city})")
			
	def getRoutesFromIata(self, iata: str) -> list[Route]:
		"""Find routes leaving from some airport"""
		try:
			sql = f"SELECT * FROM routes_coor WHERE src_iata='{iata.upper()}'"
			self.logSQL(sql)
			self.cursor.execute(sql)
		except (Exception, psycopg2.DatabaseError) as error:
			self.closeConnection(error)

		return self.getRouteListFromCursor(warningMessage = f"No routes found in getRoutesFromIata({iata.upper()})")
					
# Routes To Location Functions

	def getRoutesToCity(self, city: str) -> list[Route]:
		"""Find routes leaving from some city"""
		try:
			sql = f"""SELECT * FROM routes_coor
                    WHERE dest_city ILIKE '{city}'"""
			self.logSQL(sql)
			self.cursor.execute(sql)
			return self.getRouteListFromCursor(warningMessage = f"No routes found in getRoutesToCity({city})")
		except (Exception, psycopg2.DatabaseError) as error:
			self.closeConnection(error)
			
	def getRoutesToIata(self, iata: str) -> list[Route]:
		"""Find routes leaving from some airport"""
		try:
			sql = f"SELECT * FROM routes_coor WHERE dest_iata='{iata.upper()}'"
			self.logSQL(sql)
			self.cursor.execute(sql)
			return self.getRouteListFromCursor(warningMessage = f"No routes found in getRoutesToIata({iata.upper()})")
		except (Exception, psycopg2.DatabaseError) as error:
			self.closeConnection(error)

	def getAirlineRoutes(self, airline: str):
		"""Find routes leaving from some airport"""
		try:
			sql = f"SELECT * FROM routes_coor WHERE airline='{airline.upper()}'"
			self.logSQL(sql)
			self.cursor.execute(sql)
			return self.getRouteListFromCursor(warningMessage = f"No routes found in getRoutesToIata({airline.upper()})")
		except (Exception, psycopg2.DatabaseError) as error:
			self.closeConnection(error)


	def getRouteListFromCursor(self, warningMessage: str = None) -> list[Route]:
		"""Creates and returns a list of Routes from all routes 
            (airline, src_iata, dest_iata, src_lat, src_long, dest_lat dest_long) currently in cursor"""
		routesInCursor: list[Route] = []

		for route in self.cursor.fetchall():
			if route is None and warningMessage is not None:
				self.warning(warningMessage)
			else:
				routeFound = Route(
                    airline=route[0],
                    src_iata=route[1],
                    src_lat=route[2],
                    src_long=route[3],
                    dest_iata=route[4],
                    dest_lat=route[5],
                    dest_long=route[6],
                )
				routesInCursor.append(routeFound)

		return routesInCursor

	def closeConnection(self, message = None):
		if message is not None:
			print("\n", message, sep='')
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
