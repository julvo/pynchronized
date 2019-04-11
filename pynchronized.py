import inspect
import threading
import multiprocessing
import functools
import time

def synchronized(obj, multiprocess=True, lock=None):
    """ 
    Decorates a class, function or method to make it syncronized.

    For a class this means only one method can be executed at a time, for a 
    function this means the function can be only executed once at a time.
    """
    if lock == None:
        lock = multiprocessing.RLock() if multiprocess else threading.RLock()

    if inspect.isfunction(obj):
        obj.__lock__ = lock

        def sync_func(*args, **kwargs):
            with lock:
                return obj(*args, **kwargs)

        return sync_func

    elif inspect.isclass(obj):
        if not hasattr(obj, '__init__'):
            orig_init = lambda self: ()
        else:
            orig_init = obj.__init__

        def __init__(self, *args, **kwargs):
                self.__lock__ = lock
                orig_init(self, *args, **kwargs)
        obj.__init__ = __init__

        for key, val in obj.__dict__.items():
            if inspect.isfunction(val):
                setattr(obj, key, synchronized(val, multiprocess, lock))

    return obj

thread_synchronized = functools.partial(synchronized, multiprocess=False)
