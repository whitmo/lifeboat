from functools import wraps
from evergreen.channel import Channel

"""
python *can* do that
"""

def coro(func):
    @wraps(func)
    def start(*args,**kwargs):
        cr = func(*args,**kwargs)
        cr.next()
        return cr
    return start


def message_executor(actor, message, args, kwargs):
    callable = actor
    if message is not None:
        callable = getattr(actor, message)
    return apply(callable, *args, **kwargs)


@coro
def monologue(ctor, args, kwargs, process_msg=message_executor):
    """
    Contained single direction execution
    """
    actor = ctor(*args, **kwargs)
    while True:
        message, args, kwargs = (yield)
        process_msg(actor, message, args, kwargs)


class goro(object):
    """
    Contained bidirectional execution, based conceptually on the goroutine
    """
    def __init__(self, func, channel_ctor=Channel):
        self.func = func
        self.channel = channel_ctor()
        self.recv = self.channel.receive
        wraps(func)(self.coro)
        self.__call__ = self.coro

    def send(self, message, *args, **kwargs):
        self.cr.send((message, args, kwargs))
        self.channel.recv()

    def send_async(self, message, *args, **kwargs):
        """
        """
        self.cr.send((message, args, kwargs))
        return self.recv

    def coro(self, *args, **kwargs):
        args = self.channel, + args
        cr = self.cr = self.func(*args, **kwargs)
        cr.next()
        return cr


@goro
def go(channel, ctor, args, kwargs):
    """
    
    """
    actor = ctor(*args, **kwargs)
    while True:
        message, args, kwargs = (yield)
        message, args, kwargs = getattr(actor, message)(*args, **kwargs)
        channel.send((message, args, kwargs))





"""
STM
"""
