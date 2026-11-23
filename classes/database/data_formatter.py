def sort_by(data, key_name="", reverse=False):
    return sorted(data, key=lambda item: getattr(item, key_name), reverse=reverse)

def exclude(data, **kwargs):
    """Returns elements that do not include specified arguments"""
    excluded = []
    for item in data:
        matching = True
        for key, value in kwargs.items():
            if getattr(item, key) == value:
                matching = False
            break
        if matching: excluded.append(item)
    return excluded

def select(data, **kwargs):
    """Returns elements that include all of specified arguments"""
    selected = []
    for item in data:
        matching = True
        for key, value in kwargs.items():
            if getattr(item, key) != value:
                matching = False
                break
        if matching: selected.append(item)
    return selected

def contains(data, **kwargs):
    """Returns elements that include any of specified arguments"""
    contains = []
    for item in data:
        matching = True
        for key, value in kwargs.items():
            if value not in getattr(item, key):
                matching = False
                break
        if matching: contains.append(item)
    return contains