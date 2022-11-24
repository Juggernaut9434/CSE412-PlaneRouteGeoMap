from configparser import ConfigParser
import os

def config(filename='database.ini'):
    parser = ConfigParser()
    path = os.path.join('application', 'src', 'back_end', filename)
    print('__file__={0:<35} | __name__={1:<25} | __package__={2:<25}'.format(__file__,__name__,str(__package__)))
    parser.read(path)
    db = {} # Create empty dictionary to store and return arguments

    assert parser.has_section('postgresql'), f"Cannot find postgresql section in provided {filename}"
    params = parser.items('postgresql')

    for param in params:
        db[param[0]] = param[1]     # db['host'] = 'localhost' for example (first line in .ini)

    return db