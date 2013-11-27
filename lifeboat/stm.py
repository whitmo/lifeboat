from .thirdparty import reify
from ZODB.DB import DB
from ZODB.MappingStorage import MappingStorage
from ZODB.POSException import ConflictError
from evergreen.local import local
import logging
import transaction

logger = logging.getLogger(__name__)

class Atomic(object):
    taskstate = local()
    _dbs = {}

    @reify
    def db(self):
        tsdb = self._dbs.get(self.name, None)
        if tsdb is None:
            tsdb = self._dbs[self.name] = self.make_db(self.name)
        return tsdb

    def __init__(self, name='data', attempts=3):
        self.name = name
        self.txn = None
        self.root = None
        self.cxn = None
        self.last_commit_succeeded = None
        self.attempts = attempts

    def clear(self):
        self.txn = None
        self.root = None
        self.cxn = None

    def __enter__(self):
        self.cxn = connection = self.db.open()
        self.root = connection.root()
        self.txn = transaction.begin()
        return self.root

    def __exit__(self, etype, exc, tb):
        if exc is not None:
            transaction.abort()
            self.last_commit_succeeded = False
            raise exc

        try:
            transaction.commit()
            self.last_commit_succeeded = True
            logger.debug('GOOD')
        except ConflictError:
            logger.debug('ECONFLICT: %s', transaction.get())
            self.last_commit_succeeded = False

        self.clear()

    @staticmethod
    def make_db(name='STM'):
        """
        @@ make it durable?
        @@ make storage cofigurable?
        """
        store = MappingStorage(name=name)
        db = DB(store)
        return db
