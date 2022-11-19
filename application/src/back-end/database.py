import psycopg2
from config import config
# psycopg2 Documentation: https://www.psycopg.org/docs/index.html

def connectDB():
	conn = None
	try:
		# Connect to database
		conn = psycopg2.connect(**config())

		# Create cursor
		cursor = conn.cursor()

		# Execute SELECT version() and print result
		print("PostgreSQL database version:")
		cursor.execute('SELECT version()')
		db_version = cursor.fetchone()
		print(db_version, end="\n\n")

		# Execute COUNT of ROUTE
		print("Executing 'SELECT COUNT(*) FROM \"route\"")
		cursor.execute('SELECT COUNT(*) FROM "route"')
		count = cursor.fetchone() # fetchone() gets first row from query result
		print(count[0], end="\n\n")

		# Get all ROUTE from PHX
		print("Getting all ROUTES leaving from PHX")
		cursor.execute('SELECT * FROM "route" WHERE src_airport = \'PHX\'')
		manualCountLol = 0 # Could use another Query with COUNT(*) instead of *

		# Iterate through all output rows (NOTE: I can't tell a difference in "in cursor:" and "in cursor.fetchall():")
		for line in cursor:
			print(line)
			manualCountLol += 1

		print("Routes found: {}".format(manualCountLol), end="\n\n")

		# Close database connection
		cursor.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
			if conn is not None:
				conn.close()
				print("Database connection closed.")


if __name__ == '__main__':
	connectDB()