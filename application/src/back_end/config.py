from configparser import ConfigParser
import os

def config(filename='database.ini'):
    parser = ConfigParser()
    path = os.path.join('application', 'src', 'back_end', filename)
    parser.read(path)
    db = {} # Create empty dictionary to store and return arguments

    if not parser.has_section('postgresql'):
        print(f"Cannot find postgresql section in provided {filename}")
        return None
    
    params = parser.items('postgresql')

    for param in params:
        db[param[0]] = param[1]     # db['host'] = 'localhost' for example (first line in .ini)

    return db
