import json

# TODO : Merge base code with models.py

def get_decks(conn):
    # Return all decks as deck objects
    data = get_decks_data(conn)
    output = []
    for did in data.keys():
        output.append(Deck(data[did]))
    return output

def get_deck(conn, did):
    # Return a Model object for a given mid
    did = str(did)
    data = get_decks(conn)
    if did in data.keys():
        return Deck(data[did])
    else:
        return

def get_decks_data(conn):
    # Return data for all decks
    # Query DB for Models info
    cursor = conn.cursor()
    cursor.execute('SELECT decks FROM col LIMIT 1')
    result = cursor.fetchone()
    data = json.loads(result[0])
    return data

class Deck:
    def __init__(self, data):
        self.data = data

    @property
    def name(self):
        return self.data['name']

    @property
    def id(self):
        return self.data['id']
