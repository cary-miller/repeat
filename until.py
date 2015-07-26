'''
Needs lots of documentation.   Examples.
'''
import functools



def repeat_until_satisfied(ok, max_tries=5, 
        bad_outcome = lambda mt, r, *a, **k: 'no good result: %s attempts' % mt,
        report      = lambda *a, **k: None,
        end_of_loop = lambda *a, **k: None,
    ): 
    '''
    ok:  a predicate,  returns truthiness.
    max_tries: int > 0
    bad_outcome: a function,    default: message string
    report: a function,         default == no op
    end_of_loop: a function,    default: no op
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
            return bad_outcome(max_tries, result, *pos, **kw)
        return inner
    return outer



class Repeat(object):
    class Until(object):
        satisfied = staticmethod(repeat_until_satisfied)
    until = Until()

repeat = Repeat()
until_satisfied = repeat_until_satisfied
satisfied = repeat_until_satisfied
ok = lambda res:res

@repeat_until_satisfied(ok)
def one():
    return 1

@until_satisfied(ok)
def two():
    return 2

@repeat.until.satisfied(ok)
def three():
    return 3

def bun():
    return 'b'


