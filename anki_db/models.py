import json

def get_model(conn, mid):
    # Return a Model object for a given mid
    mid = str(mid)
    data = get_models(conn)
    if mid in data.keys():
        return Model(data[mid])
    else:
        return

def get_models(conn):
    # Return all models in DB
    # Query DB for Models info
    cursor = conn.cursor()
    cursor.execute('SELECT models FROM col LIMIT 1')
    result = cursor.fetchone()
    data = json.loads(result[0])
    return data

class Model:
    def __init__(self, data):
        self.data = data

    @property
    def name(self):
        return self.data['name']

    @property
    def templates(self):
        return self.data['tmpls']

    @property
    def template_count(self):
        return len(self.templates)

    @property
    def mid(self):
        return self.data['id']
