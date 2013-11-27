from ZODB.DB import DB
from ZODB.MappingStorage import MappingStorage
from evergreen.local import local
import transaction
from .thirdparty import reify


class Atomic(object):
    taskstate = local()
    _dbs = {}

    @reify
    def db(self):
        tsdb = self._dbs.get(self.name, None)
        if tsdb is None:
            tsdb = self._dbs[self.name] = self.make_db(self.name)
        return tsdb

    def __init__(self, name='data'):
        self.name = name
        self.txn = None

    def __enter__(self):
        self.cxn = connection = self.db.open()
        self.root = connection.root()
        self.txn = transaction.begin()
        #self.txn.join(connection)
        return self.root

    def __exit__(self, etype, exc, tb):
        if exc is not None:
            transaction.abort()
            raise exc
        transaction.commit()

    @staticmethod
    def make_db(name='STM'):
        """
        @@ make it durable?
        @@ make storage cofigurable?
        """
        store = MappingStorage(name=name)
        db = DB(store)
        return db
