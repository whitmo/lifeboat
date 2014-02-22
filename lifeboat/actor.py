from evergreen.channel import Channel
from functools import wraps
from functools import partial
import logging


logger = logging.getLogger(__name__)


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
    return apply(callable, args, kwargs)


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
        wraps(func)(self)

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

    __call__ = coro


debug_log = partial(logger.debug, 'Message: %s args: %s kwargs: %s')

def go_init(actor, no_method=None, log=logger.debug, args=[], kwargs={}):
    """
    Default function for preparing a goroutines initial state (actor, default dispatch, etc)
    """
    if not getattr(actor, '_go_init', True) and callable(actor):
        actor = actor(*args, **kwargs)
    elif any((args, kwargs)):
        log("Initialized arguments passed for pre-initialized actor args: %s, kwargs: %s")

    default_dispatch = debug_log
    if isinstance(no_method, basestring):
        default_dispatch = getattr(actor, no_method, None)

    if callable(no_method):
        default_dispatch = no_method
    return actor, default_dispatch


@goro
def go(channel, actor, init=go_init,
       no_method=None, def_method=debug_log,
       logger=logger, args=tuple(), **kwargs):
    """
    A coro that send to a Channel

    :arg actor_ctor: A object or a callable returning an object whose
                     methods match the channel methods.

    :arg args: Optional iterable of arguments for the actor constructor

    :arg kwargs: Optional keyword that will be passed to the actor constructor
    """
    actor,
    default_dispatch = init(actor,
                            no_method=no_method,
                            log=logger.debug,
                            args=args, kwargs=kwargs)
    while True:
        message, args, kwargs = (yield)
        handler = getattr(actor, message, False) or default_dispatch
        message, args, kwargs = handler(message, *args, **kwargs)
        channel.send((message, args, kwargs))
