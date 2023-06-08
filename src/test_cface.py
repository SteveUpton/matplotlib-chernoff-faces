from cface import cface

def test_always_passes():
    ax = {}
    actual = cface(ax)
    assert actual == ax
