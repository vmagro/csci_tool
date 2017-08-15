# print tests by their docstring, not function name
def pytest_itemcollected(item):
    node = item.obj
    suf = node.__doc__.strip() if node.__doc__ else node.__name__
    if suf:
        item._nodeid = suf
