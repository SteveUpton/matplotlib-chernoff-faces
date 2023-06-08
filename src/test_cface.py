import matplotlib.pyplot as plt
from cface import cface

def test_ticks_removed():
    fig, axes = plt.subplots()
    ax = cface(axes)
    assert ax.get_xticks().size == 0
    assert ax.get_yticks().size == 0
