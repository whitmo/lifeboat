from ZODB.MappingStorage import MappingStorage
from ZODB.DB import DB
from evergreen.local import local


class Atomic(object):
    taskstate = local()
    taskstate.db = None

    @property
    def root(self):
        tsdb = self.taskstate.db
        if tsdb is None:
            self.taskstate.db = self.dbroot()
        return tsdb

    def __init__(self):
        pass

    def __enter__(self):
        pass

    def __exit__(self, *args, **kwargs):
        pass

    @staticmethod
    def dbroot(name='STM'):
        """
        @@ make it durable?
        @@ make storage cofigurable?
        """
        store = MappingStorage(name=name)
        db = DB(store)
        connection = db.open()
        root = connection.root()
        return root
