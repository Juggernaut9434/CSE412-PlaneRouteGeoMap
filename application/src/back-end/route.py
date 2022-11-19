class Route():
    """Contains information used for putting a route on the map
    includes: airline,
                        src_iata, src_lat, src_long from src_airport,
                        dest_iata, dest_lat, dest_long from dest_airport"""
    airline = ""
    src_iata, src_lat, src_long, dest_iata, dest_lat, dest_long = 0, 0, 0, 0, 0, 0

    def __init__(self, airline, src_iata, src_lat, src_long, dest_iata, dest_lat, dest_long) -> None:
        self.airline = airline
        self.src_iata = src_iata
        self.src_lat = src_lat
        self.src_long = src_long
        self.dest_iata = dest_iata
        self.dest_lat = dest_lat
        self.dest_long = dest_long

    def getSource(self):
        """Returns source tuple (latitude, longitude) for mapping"""
        return (self.src_lat, self.src_long)

    def getDestination(self):
        """Returns destination tuple (latitude, longitude) for mapping"""
        return (self.dest_lat, self.dest_long)