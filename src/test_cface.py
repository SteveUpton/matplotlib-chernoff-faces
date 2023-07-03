import matplotlib.pyplot as plt
import pandas as pd
import pytest

from cface import CFace

class TestCFace:

    def test_sets_default_feature_values(self):
        cface = CFace()
        assert cface.features['nose_width'] == CFace.feature_ranges['nose_width']['default']
        assert cface.features['nose_length'] == CFace.feature_ranges['nose_length']['default']
        assert cface.features['head_width'] == CFace.feature_ranges['head_width']['default']
        assert cface.features['head_length'] == CFace.feature_ranges['head_length']['default']
        assert cface.features['eye_width'] == CFace.feature_ranges['eye_width']['default']
        assert cface.features['eye_length'] == CFace.feature_ranges['eye_length']['default']
        assert cface.features['eye_spacing'] == CFace.feature_ranges['eye_spacing']['default']
        assert cface.features['eye_height'] == CFace.feature_ranges['eye_height']['default']
        assert cface.features['eye_angle'] == CFace.feature_ranges['eye_angle']['default']
        assert cface.features['pupil_size'] == CFace.feature_ranges['pupil_size']['default']
        assert cface.features['mouth_length'] == CFace.feature_ranges['mouth_length']['default']
        assert cface.features['mouth_height'] == CFace.feature_ranges['mouth_height']['default']
        assert cface.features['eyebrow_length'] == CFace.feature_ranges['eyebrow_length']['default']
        assert cface.features['eyebrow_angle'] == CFace.feature_ranges['eyebrow_angle']['default']
        assert cface.features['eyebrow_height'] == CFace.feature_ranges['eyebrow_height']['default']

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

        assert cface.features['nose_width'] == 0.01
        assert cface.features['nose_length'] == 0.02
        assert cface.features['head_width'] == 0.03
        assert cface.features['head_length'] == 0.04
        assert cface.features['eye_width'] == 0.05
        assert cface.features['eye_length'] == 0.06
        assert cface.features['eye_spacing'] == 0.07
        assert cface.features['eye_height'] == 0.08
        assert cface.features['eye_angle'] == 0.09
        assert cface.features['pupil_size'] == 0.10
        assert cface.features['mouth_length'] == 0.11
        assert cface.features['mouth_height'] == 0.12
        assert cface.features['eyebrow_length'] == 0.13
        assert cface.features['eyebrow_angle'] == 0.14
        assert cface.features['eyebrow_height'] == 0.15

            
    def test_rejects_features_too_small(self):
        with pytest.raises(ValueError):
            CFace(nose_width=-0.1,
                  nose_length=-0.1,
                  head_width=-0.1,
                  head_length=-0.1,
                  eye_width=-0.1,
                  eye_length=-0.1,
                  eye_spacing=-0.1,
                  eye_height=-0.1,
                  eye_angle=-0.1,
                  pupil_size=-0.1,
                  mouth_length=-0.1,
                  mouth_height=-0.1,
                  eyebrow_length=-0.1,
                  eyebrow_angle=-0.1,
                  eyebrow_height=-0.1)

    def test_rejects_features_too_large(self):
        with pytest.raises(ValueError):
            CFace(nose_width=1.1,
                  nose_length=1.1,
                  head_width=1.1,
                  head_length=1.1,
                  eye_width=1.1,
                  eye_length=1.1,
                  eye_spacing=1.1,
                  eye_height=1.1,
                  eye_angle=1.1,
                  pupil_size=1.1,
                  mouth_length=1.1,
                  mouth_height=1.1,
                  eyebrow_length=1.1,
                  eyebrow_angle=1.1,
                  eyebrow_height=1.1)

class TestCFacePlot:

    def test_ticks_removed(self):
        cface = CFace()
        fig, axes = plt.subplots()
        ax = cface.plot(axes)
        assert ax.get_xticks().size == 0
        assert ax.get_yticks().size == 0

    def test_sets_axis_limits(self):
        cface = CFace()
        fig, axes = plt.subplots()
        ax = cface.plot(axes)
        assert ax.get_xlim() == (-1.0, 1.0)
        assert ax.get_ylim() == (-1.0, 1.0)

    def test_does_not_set_axis_title_if_none_supplied(self):
        cface = CFace()
        fig, axes = plt.subplots()
        ax = cface.plot(axes)
        assert ax.get_title(loc='left') == ''

    def test_does_sets_axis_title(self):
        cface = CFace()
        fig, axes = plt.subplots()
        ax = cface.plot(axes, 'Name')
        assert ax.get_title(loc='left') == 'Name'

class TestScaleFeature:

    def test_scales_feature_given_0_1_range(self):
        scaled_feature = CFace._scale_feature(0.5, new_min=0, new_max=1)
        assert scaled_feature ==  0.5

    def test_scales_feature_given_0_100_range(self):
        scaled_feature = CFace._scale_feature(0.7, new_min=0, new_max=100)
        assert scaled_feature ==  70

    def test_scales_feature_given_negative_range(self):
        scaled_feature = CFace._scale_feature(0.3, new_min=-100, new_max=100)
        assert scaled_feature ==  -40

    def test_scales_to_max_of_range(self):
        scaled_feature = CFace._scale_feature(1, new_min=0, new_max=1)
        assert scaled_feature ==  1

    def test_scales_to_min_of_range(self):
        scaled_feature = CFace._scale_feature(0, new_min=0, new_max=1)
        assert scaled_feature ==  0

class TestNormaliseDF:

    @pytest.fixture
    def df_simple(self):
        return pd.DataFrame([[1, 2], [1, 1]], columns=['A', 'B'])

    @pytest.mark.usefixtures('df_simple')
    def test_returns_dataframe(self, df_simple):
        prepped_df, feature_map = CFace.normalise_df(df_simple)
        assert type(prepped_df) is pd.core.frame.DataFrame

    @pytest.mark.usefixtures('df_simple')
    def test_all_values_in_range_0_1(self, df_simple):
        prepped_df, feature_map = CFace.normalise_df(df_simple)
        for column in prepped_df:
            assert prepped_df[column].min() >= 0
            assert prepped_df[column].max() <= 1

    @pytest.mark.usefixtures('df_simple')
    def test_returns_feature_map_with_all_keys(self, df_simple):
        prepped_df, feature_map = CFace.normalise_df(df_simple)
        assert list(feature_map.values()) == prepped_df.columns.values.tolist()

class TestCreateCfaceFromRow:
    
    @pytest.fixture
    def feature_map_numeric_col_names(self):
        return {
            'nose_width': 0,
            'nose_length': 1,
            'head_width': 2,
            'head_length': 3,
            'eye_width': 4,
            'eye_length': 5,
            'eye_spacing': 6,
            'eye_height': 7,
            'eye_angle': 8,
            'pupil_size': 9,
            'mouth_length': 10,
            'mouth_height': 11,
            'eyebrow_length': 12,
            'eyebrow_angle': 13,
            'eyebrow_height': 14    
        }

    def test_returns_cface(self):
        cface = CFace.create_cface_from_row({}, {})
        assert type(cface) is CFace

    @pytest.mark.usefixtures('feature_map_numeric_col_names')
    def test_returns_cface_2(self, feature_map_numeric_col_names):
        cface = CFace.create_cface_from_row(pd.Series([0.01, 0.02, 0.03, 0.04, 0.05,
                                                       0.06, 0.07, 0.08, 0.09, 0.10,
                                                       0.11, 0.12, 0.13, 0.14, 0.15]),
                                                       feature_map_numeric_col_names)
        assert cface.features['nose_width'] == 0.01
        assert cface.features['nose_length'] == 0.02
        assert cface.features['head_width'] == 0.03
        assert cface.features['head_length'] == 0.04
        assert cface.features['eye_width'] == 0.05
        assert cface.features['eye_length'] == 0.06
        assert cface.features['eye_spacing'] == 0.07
        assert cface.features['eye_height'] == 0.08
        assert cface.features['eye_angle'] == 0.09
        assert cface.features['pupil_size'] == 0.10
        assert cface.features['mouth_length'] == 0.11
        assert cface.features['mouth_height'] == 0.12
        assert cface.features['eyebrow_length'] == 0.13
        assert cface.features['eyebrow_angle'] == 0.14
        assert cface.features['eyebrow_height'] == 0.15

class TestNormaliseValue:

    def test_maintains_value_when_range_0_1(self):
        normalised_value = CFace._normalise_value(value=0.5, old_min=0, old_range=1)
        assert normalised_value == 0.5

    def test_returns_1_when_range_0(self):
        normalised_value = CFace._normalise_value(value=0.5, old_min=0, old_range=0)
        assert normalised_value == 1

    def test_normalises_value(self):
        normalised_value = CFace._normalise_value(value=50, old_min=0, old_range=100)
        assert normalised_value == 0.5

    def test_normalises_negative_value(self):
        normalised_value = CFace._normalise_value(value=-0.5, old_min=-1, old_range=1)
        assert normalised_value == 0.5
