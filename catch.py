import functools


def catch(Exc, action=lambda E,e: (E, e), reraise=True, default=None, *a, **k): 
    '''
    Catch a fatal exception and perform some action.
    Q.  return something if not reraising?
    NOTE reraise overrides default
    '''
    def outer(func):
        @functools.wraps(func)
        def inner(*pos, **kw):
            try:
                return func(*pos, **kw)
            except Exc, exc:
                action(Exc, exc)
                if reraise:
                    raise
                elif default:
                    return default(func, E, e, action, *pos, **kw)
        return inner
    return outer


#def catch(Exc, action=lambda E,e: (E, e), reraise=True, *a, **k): 

def f5():
    return 1/0

@catch(ZeroDivisionError, reraise=False)
def f6():
    return 1/0

@catch(ZeroDivisionError, action=logit, reraise=False)
def f7():
    return 1/0




def repeat_until_no_exception(Exc, max_tries=5, 
        bad_outcome = lambda mt, r, *a, **k: 'no good result: %s attempts' % mt,
        report      = lambda *a, **k: None,
        end_of_loop = lambda *a, **k: None,
    ): 
    '''
    Arguments:
        Exc:  Exception
        max_tries: int > 0
        bad_outcome: a function,    default: message string
        report: a function,         default == no op
        end_of_loop: a function,    default: no op

    Return:
        a decorator!
    '''
    def outer(func):
        @functools.wraps(func)
        def inner(*pos, **kw):
            i = 0
            while i < max_tries:
                i += 1
                try:
                    return func(*pos, **kw)
                except Exc, exc:
                    report(func, i, max_tries, result, *pos, **kw)
                end_of_loop(i, max_tries, result, *pos, **kw)
            return bad_outcome(max_tries, result, *pos, **kw)
        return inner
    return outer


