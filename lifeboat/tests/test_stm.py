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
