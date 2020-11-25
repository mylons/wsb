import sqlite3


class Stocks:

    def __init__(self):
        self.db = 'stocks.db'

    def _query(self, q):
        with sqlite3.connect(self.db) as cnx:
            return cnx.execute(q).fetchall()

    def nyse(self):
        return [q[0] for q in self._query('select Symbol from nyse')]

    def amex(self):
        return [q[0] for q in self._query('select Symbol from amex')]

    def nasdaq(self):
        return [q[0] for q in self._query('select Symbol from nasdaq')]


from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
"""
Base = declarative_base()
engine = create_engine('sqlite:///:memory:', echo=True)


class Posts(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    post_id = Column(String)
    content = Column(Text)


Base.metadata.create_all(engine)
"""
MOST_COMMON_WORDS = frozenset({'good',
                               'Best',
                               'Rs',
                               'Eat',
                               'Are',
                               'pump',
                               'age',
                               'man',
                               'Now',
                               'k',
                               'Mc',
                               'Hope',
                               'bit',
                               'out',
                               'six',
                               'well',
                               'play',
                               'peak',
                               'form',
                               'Turn',
                               'Ha',
                               'go',
                               'He',
                               'it',
                               'life',
                               'trip',
                               'care',
                               'On',
                               'An',
                               'oi',
                               'par',
                               'wins',
                               'hear',
                               'loan',
                               'OGs',
                               'see',
                               'Plus',
                               'are',
                               'one',
                               'Well',
                               'do',
                               'tell',
                               'fam',
                               'coke',
                               'big',
                               'new',
                               'It',
                               'Am',
                               'very',
                               'home',
                               'next',
                               'air',
                               'lite',
                               'One',
                               'nice',
                               'Bro',
                               'plan',
                               'pack',
                               'work',
                               'eh',
                               'Can',
                               'all',
                               'fr',
                               'Man',
                               'For',
                               'alt',
                               'pro',
                               'By',
                               'for',
                               'bill',
                               'any',
                               'At',
                               'Any',
                               'he',
                               'or',
                               'low',
                               'r',
                               'Or',
                               'mod',
                               'job',
                               'ship',
                               'cash',
                               'Wow',
                               'info',
                               'love',
                               'glad',
                               'so',
                               'ten',
                               'Tree',
                               'i',
                               'land',
                               'live',
                               'can',
                               'be',
                               'hope',
                               'else',
                               'Glad',
                               'Home',
                               'fun',
                               'an',
                               'Good',
                               'at',
                               'So',
                               'cake',
                               'Do',
                               'jack',
                               'sum',
                               'stay',
                               'twin',
                               'eat',
                               'save',
                               'Nice',
                               'hi',
                               'now',
                               'Big',
                               'auto',
                               'dd',
                               'blue',
                               'best',
                               'ago',
                               'ino',
                               'gain',
                               'real',
                               'dare',
                               'ide',
                               'fund',
                               'am',
                               'old',
                               'bro',
                               'Go',
                               'two',
                               'hook',
                               'hes',
                               'ever',
                               'by',
                               'grow',
                               'self',
                               'See',
                               'on',
                               'Very',
                               'All',
                               'has',
                               'per',
                               'Hi',
                               'mind',
                               'huge',
                               'I',
                               'a',
                               'IRS',
                               'irs'})

