import matplotlib.pyplot as plt
import pandas as pd
import pytest

from cface import cface

@pytest.fixture
def df_row_simple():
    return pd.DataFrame([[1, 2]], columns=['A', 'B']).loc[0]

def test_ticks_removed():
    fig, axes = plt.subplots()
    ax = cface(axes, df_row_simple)
    assert ax.get_xticks().size == 0
    assert ax.get_yticks().size == 0

def test_rejects_missing_row():
    with pytest.raises(TypeError):
        fig, axes = plt.subplots()
        ax = cface(axes)

def test_accepts_row():
    fig, axes = plt.subplots()
    ax = cface(axes, df_row_simple)
    assert ax