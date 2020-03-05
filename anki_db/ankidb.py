import sqlite3
import os
import csv
from collections import namedtuple

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

    
