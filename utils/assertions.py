

def assert_equal(val_1, val_2):
    """ """
    if val_1 == val_2:
        return True
    return False


def assert_unequal(val_1, val_2):
    """ """
    if val_1 != val_2:
        return True
    return False


def assert_true(condition):
    """ """
    if condition:
        return True
    return False


def assert_false(condition):
    """ """
    if not condition:
        return True
    return False
