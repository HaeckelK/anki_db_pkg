import sqlite3
import os
import csv
from collections import namedtuple

from . import utils

ReviewRow = namedtuple('ReviewRow', ('id', 'cid', 'usn', 'ease', 'ivl',
                               'lastIvl', 'factor', 'time', 'type'))
CardRow = namedtuple('CardRow', ('id','nid','did','ord','mod','usn',
                                 'type','queue','due','ivl','factor',
                                 'reps','lapses','left','odue','odid',
                                 'flags','data'))


def _get_tables(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT name from sqlite_master where type="table"')
    return tuple(x[0] for x in cursor.fetchall())


def _table_data(conn, table):
    cursor = conn.execute('SELECT * FROM ' + table)
    names = [description[0] for description in cursor.description]
    data = cursor
    return names, data


def _table_to_csv(conn, table, folder):
    names, data = _table_data(conn, table)
    filename = _export_csv(data, names, table, folder)
    return filename


def _export_csv(data, columns, table, folder):
    filename = os.path.join(folder, table + '.csv')
    with open(filename, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(columns)
        writer.writerows(data)
    return filename


class NewNote():
    def __init__(self, conn, mid, fields, did):
        # mid must exist!
        self.conn = conn
        self.id = utils.intTime(1000)
        self.guid = utils.guid64()
        self.mid = mid
        self.mod = utils.intTime() # Why no 1000?
        self.usn = -1 # Indicates change needs to be pushed to server?
        self.fields = fields # Need to be separated by special character
        self.flags = 0 # Unused
        self.data = '' # Unused
        self.did = did
        
        return

    def add(self, commit=True):
        print('Add NewNote')
        print('Deck:', self.did)
        print('Model:', self.mid)
        # csum is used to check that note doesn't already exist.
        # I have not yet replicated this functionality
        csum = utils.fieldChecksum(self.fields[0])
        tags = '' # Leave blank for now
        fields = utils.joinFields(self.fields)
        sfld = self.fields[0] # This is not correct
        res = self.conn.cursor().execute(
            """
insert or replace into notes values (?,?,?,?,?,?,?,?,?,?,?)""",(
            self.id,
            self.guid,
            self.mid,
            self.mod,
            self.usn,
            tags,
            fields,
            sfld,
            csum,
            self.flags,
            self.data
        ))
        output = {self.id: []}
        # TODO : Different number for Cloze cards?
        # TODO : Ord from mid
        ord_max = 2
        for ord in range(ord_max):
            cardid = self._add_card(nid=self.id, did=self.did, ord=ord)
            output[self.id].append(cardid)
        if commit:
            self.conn.commit()
        return output

    def _add_card(self, nid, did, ord):
        # TODO : How many? Need to add type Number? (into card?) Ord?
        card = NewCard(self.conn, nid, did, ord)
        cardid = card.add(commit=False)
        return cardid

class NewCard:
    def __init__(self, conn, nid, did, ord):
        self.conn = conn
        self.ord = ord
        self.id = utils.intTime(1000) # Does this need the 1000?
        self.nid = nid
        self.did = did
        self.ord = 0
        self.mod = utils.intTime()
        self.usn = -1
        self.type = 0
        self.queue = 0
        self.due = 0
        self.ivl = 0
        self.factor = 0
        self.reps = 0
        self.lapses = 0
        self.left = 0
        self.odue = 0
        self.odid = 0
        self.flags = 0
        self.data = ''
        return

    def add(self, commit=True):
        print('Add NewCard')
        print('Note:', self.nid)
        print('Deck:', self.did)
        res = self.conn.cursor().execute(
            """
insert or replace into cards values
(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",(
            self.id,
            self.nid,
            self.did,
            self.ord,
            self.mod,
            self.usn,
            self.type,
            self.queue,
            self.due,
            self.ivl,
            self.factor,
            self.reps,
            self.lapses,
            self.left,
            self.odue,
            self.odid,
            self.flags,
            self.data)
        )
        if commit:
            self.conn.commit()
        return self.id

class Ankidb():
    expected_tables = ('col', 'notes', 'cards', 'revlog', 'graves',
                       'sqlite_stat1')
    def __init__(self, path):
        """
        path : str
            Full path to Anki Database
        """
        assert isinstance(path, str)
        assert os.path.exists(path)
        self.path = path
        self.conn = sqlite3.connect(self.path)
        assert self.tables == self.expected_tables
        return

    def close(self):
        self.conn.close()
        return
    
    @property
    def tables(self):
        return _get_tables(self.conn)

    def to_csv_all(self, folder):
        print('Saving tables to csv')
        for table in self.tables:
            print(table)
            filename = _table_to_csv(self.conn, table, folder)
            print(filename)
        return

    def review_history(self, cardid):
        # Return full review lifetime of a card
        print('Review History Cardid: ', cardid)
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM revlog where cid={}'.format(cardid))
        reviews = [ReviewRow(*row) for row in cursor]
        return reviews

    def review_count(self, cardid):
        # Return number of reviews for a card
        print('Review Count Cardid: ', cardid)
        cursor = self.conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM revlog where cid={}'.format(cardid))        
        return int(cursor.fetchone()[0])

    def review_counts(self, cardids):
        # Return dict of card reviews by cardid
        data = {cardid: self.review_count(cardid) for cardid in cardids}
        return data

    def card_row(self, cardid):
        # return cardrow as tuple
        print('Cardid info: ', cardid)
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM cards where id={}'.format(cardid))
        card = [CardRow(*row) for row in cursor]        
        return card

    
