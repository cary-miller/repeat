
import functools
import inspect

def outer(func):
    def inner(*a, **k):
        return func(*a, **k)

    # A Jesse Jiryu Davis shows how to copy the argspec.
    # http://emptysqua.re/blog/copying-a-python-functions-signature/
    argspec = inspect.getargspec(func)
    formatted_args = inspect.formatargspec(*argspec)
    fndef = 'lambda %s: inner%s' % ( 
        formatted_args.lstrip('(').rstrip(')'), formatted_args)
    inner = eval(fndef, {'inner': inner})
    return functools.wraps(func)(inner)

