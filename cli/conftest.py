# print tests by their docstring, not function name
def pytest_itemcollected(item):
    node = item.obj
    if node.__doc__:
        suf = node.__doc__.strip()
    elif hasattr(node, '__name__'):
        suf = node.__name__
    else:
        suf = '<no name>'
    if suf:
        item._nodeid = suf
