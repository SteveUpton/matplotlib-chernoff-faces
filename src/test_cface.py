import matplotlib.pyplot as plt
import pandas as pd
import pytest

from cface import cface

@pytest.fixture
def df_row_simple():
    return pd.DataFrame([[1, 2]], columns=['A', 'B']).loc[0]

@pytest.mark.usefixtures('df_row_simple')
def test_ticks_removed(df_row_simple):
    fig, axes = plt.subplots()
    ax = cface(axes, df_row_simple)
    assert ax.get_xticks().size == 0
    assert ax.get_yticks().size == 0

def test_rejects_missing_row():
    with pytest.raises(TypeError):
        fig, axes = plt.subplots()
        ax = cface(axes)

@pytest.mark.usefixtures('df_row_simple')
def test_accepts_row(df_row_simple):
    fig, axes = plt.subplots()
    ax = cface(axes, df_row_simple)
    assert ax

@pytest.mark.usefixtures('df_row_simple')
def test_sets_axis_title(df_row_simple):
    fig, axes = plt.subplots()
    ax = cface(axes, df_row_simple)
    assert axes.get_title(loc='left') == '0'

@pytest.mark.usefixtures('df_row_simple')
def test_sets_axis_limits(df_row_simple):
    fig, axes = plt.subplots()
    ax = cface(axes, df_row_simple)
    assert axes.get_xlim() == (-1.0, 1.0)
    assert axes.get_ylim() == (-1.0, 1.0)
