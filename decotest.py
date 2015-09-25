'''
Useful functions for testing decorators.
'''



# This test applies to any decorator and any function.
def test_decorated_attributes(decorator, func):
    '''Verify that attributes of a decorated function are same as original.
    __name__ __doc__ etc
    '''
    decorated = decorator(func)
    assert decorated.__name__ == func.__name__ 
    assert decorated.__doc__ == func.__doc__ 
    assert decorated.__module__ == func.__module__ 
    print('test_decorated_attributes ok')
    return 'ok'

    # We would like to say the parameters are identical but that will have
    # to wait for version >= 3.4.   The decorator module does it but changes
    # the decorator syntax.
    from inspect import getargspec as argspec
    assert argspec(decorated) == argspec(func)
    print('dict func', func.__dict__)
    print('dict decorated', decorated.__dict__)
    assert decorated.__dict__ != func.__dict__ 
    return 'ok'


def decorated_return_value_ok(decorator, func, close_enough, *a, **k):
    old = func(*a, **k)
    new = decorator(func)(*a, **k)
    return close_enough(old, new)
  
