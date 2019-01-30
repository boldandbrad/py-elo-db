from peewee import *

db = SqliteDatabase('./database.db', pragmas={'foreign_keys': 1})


class Base(Model):

    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):
        return str(self.__dict__)

    class Meta():
        database = db
        legacy_table_names = False
