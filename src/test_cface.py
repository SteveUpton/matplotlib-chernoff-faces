import matplotlib.pyplot as plt
import pandas as pd
import pytest

from cface import cface
from cface import CFace

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

class TestCFace:

    def test_sets_default_feature_values(self):
        cface = CFace()
        assert cface.nose_width == CFace.defaults['nose_width']
        assert cface.nose_length == CFace.defaults['nose_length']
        assert cface.head_width == CFace.defaults['head_width']
        assert cface.head_length == CFace.defaults['head_length']
        assert cface.eye_width == CFace.defaults['eye_width']
        assert cface.eye_length == CFace.defaults['eye_length']
        assert cface.eye_spacing == CFace.defaults['eye_spacing']
        assert cface.eye_height == CFace.defaults['eye_height']
        assert cface.eye_angle == CFace.defaults['eye_angle']
        assert cface.pupil_size == CFace.defaults['pupil_size']
        assert cface.mouth_length == CFace.defaults['mouth_length']
        assert cface.mouth_height == CFace.defaults['mouth_height']
        assert cface.eyebrow_length == CFace.defaults['eyebrow_length']
        assert cface.eyebrow_angle == CFace.defaults['eyebrow_angle']
        assert cface.eyebrow_height == CFace.defaults['eyebrow_height']

    def test_assigns_feature_values(self):
        cface = CFace(nose_width=0.01,
                      nose_length=0.02,
                      head_width=0.03,
                      head_length=0.04,
                      eye_width=0.05,
                      eye_length=0.06,
                      eye_spacing=0.07,
                      eye_height=0.08,
                      eye_angle=0.09,
                      pupil_size=0.10,
                      mouth_length=0.11,
                      mouth_height=0.12,
                      eyebrow_length=0.13,
                      eyebrow_angle=0.14,
                      eyebrow_height=0.15)

        assert cface.nose_width == 0.01
        assert cface.nose_length == 0.02
        assert cface.head_width == 0.03
        assert cface.head_length == 0.04
        assert cface.eye_width == 0.05
        assert cface.eye_length == 0.06
        assert cface.eye_spacing == 0.07
        assert cface.eye_height == 0.08
        assert cface.eye_angle == 0.09
        assert cface.pupil_size == 0.10
        assert cface.mouth_length == 0.11
        assert cface.mouth_height == 0.12
        assert cface.eyebrow_length == 0.13
        assert cface.eyebrow_angle == 0.14
        assert cface.eyebrow_height == 0.15
