import pandas as pd

from cface import prep_dataframe

def test_returns_dataframe():
    original_df = pd.DataFrame([[1, 2], [1, 2], [1, 2]], columns=['A', 'B'])
    prepped_df = prep_dataframe(original_df)
    assert type(prepped_df) is pd.core.frame.DataFrame

def test_returns_same_dataframe():
    original_df = pd.DataFrame([[1, 2], [1, 2], [1, 2]], columns=['A', 'B'])
    prepped_df = prep_dataframe(original_df)
    pd.testing.assert_frame_equal(original_df, prepped_df)
