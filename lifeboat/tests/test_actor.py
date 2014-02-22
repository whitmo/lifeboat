from mock import Mock
from mock import call


def test_coro():
    """
    positive coro test
    """
    from lifeboat import actor

    @actor.coro
    def set(state):
        while True:
            tag, val = (yield)
            state[tag] = val

    state = {}
    setstate = set(state)
    setstate.send(("hello", "world"))
    assert 'hello' in state


def test_message_exec():
    from lifeboat import actor

    args = ['one', 'two']
    kw = dict(hey='wat')

    def testvars(*args, **kwargs):
        assert args == args
        assert kwargs == kwargs
        return True

    theactor = Mock(side_effect=testvars)
    out = actor.message_executor(theactor, None, args, kw)
    assert out == True
    assert theactor.called
    assert theactor.call_args == call(*args, **kw)

def test_message_exec_dispatch():
    from lifeboat import actor

    args = ['one', 'two']
    kw = dict(hey='wat')

    def testvars(*args, **kwargs):
        assert args == args
        assert kwargs == kwargs
        return True

    theactor = Mock()
    theactor.a_method= Mock(side_effect=testvars)

    out = actor.message_executor(theactor, 'a_method', args, kw)
    assert out == True
    assert theactor.a_method.call_args == call(*args, **kw)
