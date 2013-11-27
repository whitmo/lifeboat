from persistent import Persistent
from threading import Thread
import logging



logger = logging.getLogger(__name__)


class Counter(Persistent):

    def __init__(self):
        self.count = 0

    def hit(self):
        self.count = self.count + 1

    # def _p_resolveConflict(self, oldState, savedState, newState):
    #     logger.info('CONFLICT')
    #     # Figure out how each state is different:
    #     savedDiff = savedState['count'] - oldState['count']
    #     newDiff = newState['count'] - oldState['count']

    #     # Apply both sets of changes to old state:
    #     return oldState['count'] + savedDiff + newDiff


class TestSTM(object):
    def makeone(self):
        from lifeboat.stm import Atomic
        return Atomic()

    def teardown(self):
        from lifeboat.stm import Atomic
        Atomic._dbs = {}

    def test_single_thread_get_set(self):
        atomic = self.makeone()
        with atomic as root:
            root['test'] = "wat"

        with atomic as root:
            assert root['test'] == "wat"

    def test_single_thread_error(self):
        atomic = self.makeone()
        try:
            with atomic as root:
                root['test'] = 'hey'
                raise Exception('KABOOM')
        except :
            pass

        with atomic as root:
            assert root.get('test') == None

    def test_multi_thread(self):
        atomic = self.makeone()
        with atomic as root:
            root['wat'] = Counter()

        t1 = Thread(target=self.callit, args=('t1',), name='t1')
        t2 = Thread(target=self.callit, args=('t2',), name='t2')
        t1.start()
        t2.start()
        t1.join(), t2.join()

        with atomic as root:
            assert root['wat'].count == 20

    def callit(self, name):
        atomic = self.makeone()
        for x in range(10):
            n = "%s-%02d" %(name, x)
            for x in range(3):
                with atomic as root:
                    root['wat'].hit()

                if atomic.last_commit_succeeded:
                    logger.info(n)
                    break
