'''
martin fowler
What did we do well?
What have we learned?
What can we do better?
What puzzles us?
http://martinfowler.com/articles/richardsonMaturityModel.html
'''


def catch(Exc, action=lambda E,e: (E, e), reraise=True, *a, **k): 
    '''
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
        return inner
    return outer


class FooE(Exception): pass


def fx():
    if random.random() < 0.05:
        raise FooE('fooey')
    return random.choice(range(11))


def f1():
    return fx()


def logit(E, e):
    print E, e


@catch(FooE, logit)
def f2():
    return fx()


@repeat_until_satisfied(lambda r: r<2, max_tries=3, report=report)
@catch(FooE, logit, False)
def f3():
    return fx()


@catch(FooE, logit, False)
@repeat_until_satisfied(lambda r: r<2, max_tries=3)
def f4():
    return fx()



