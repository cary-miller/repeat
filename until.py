import functools




def repeat_until_satisfied(ok, max_tries=5, 
        bad_outcome = lambda r, mt, *a, **k: 'no good result: %s attempts' % mt,
        report = lambda *a, **k: None,
        end_of_loop = lambda *a, **k: None,
    ): 
    '''
    ok:  a predicate,  returns truthiness.
    bad_outcome: a function
    report: a function
    end_of_loop: a function
    '''
    def outer(func):
        @functools.wraps(func)
        def inner(*pos, **kw):
            i = 0
            while i < max_tries:
                i += 1
                result = func(*pos, **kw)
                report(func, i, max_tries, result, *pos, **kw)
                if ok(result):
                    return result
                end_of_loop(i, max_tries, result, *pos, **kw)
            return bad_outcome(result, max_tries, *pos, **kw)
        return inner
    return outer


