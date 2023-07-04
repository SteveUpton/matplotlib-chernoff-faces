# matplotlib-chernoff-faces
A Python module to visualise a Pandas DataFrame or arbitrary data as Chernoff Faces, using Matplotlib.

## Installation
Coming soon
## Usage
Typically, I start data analysis by loading the data into a pandas DataFrame, so this module assumes that as a starting point. The suggested workflow is:

```python
import matplotlib.pyplot as plt
import pandas as pd

from cface import CFace

# Import your data
df = pd.read_csv('data.csv')

# Clean and filter the data you want to visualise as Chernoff Faces

# Normalise the dataframe to prepare for Chernoff Face creation
df_faces, feature_map = CFace.normalise_df(df)

# If you want to change the mapping from features to columns, now is the time
# feature_map['nose_width'] = 'column_name'

# Create a Chernoff Face for each row of the DataFrame
df_faces['cface'] = df_faces.apply(CFace.create_cface_from_row, axis=1, feature_map=feature_map)

# Visualise the Chernoff faces (this example assumes 20 rows in df_faces
fig = plt.figure(figsize=(10,8))
for i in range(len(df_faces)):
    ax = fig.add_subplot(4, 5, i+1, aspect='equal')
    df_faces.iloc[i, df_faces.columns.get_loc("cface")].plot(ax, i)

plt.show()
```

If you want to change the mapping from Chernoff Face features to columns in your DataFrame, you can edit the mappings in `feature_map` manually. Multiple features can be mapped to the same column name. If no column is specified for a given feature (ie. the feature key is missing), the feature will default to the middle of the range (0.5). If a feature is mapped to a column that does not exist in the DataFrame, a KeyError will be thrown. A complete `feature_map` is a dict that looks like this:

```python
{
    'nose_width': 'col1',
    'nose_length': 'col2',
    'head_width': 'col3',
    'head_length': 'col4',
    'eye_width': 'col5',
    'eye_length': 'col6',
    'eye_spacing': 'col7',
    'eye_height': 'col8',
    'eye_angle': 'col9',
    'pupil_size': 'col10',
    'mouth_length': 'col11',
    'mouth_height': 'col12',
    'eyebrow_length': 'col13',
    'eyebrow_angle': 'col14',
    'eyebrow_height': 'col15'    
}
```

You can also create a Chernoff Face directly:

```python
# Create a Chernoff Face, specifying which features (range: 0-1) you want to change
cface = CFace(nose_width = 1,
              nose_length = 1,
              head_width = 1,
              head_length = 1,
              eye_width = 1,
              eye_length = 1,
              eye_spacing = 1,
              eye_height = 1,
              eye_angle = 1,
              pupil_size = 1,
              mouth_length = 1,
              mouth_height = 1,
              eyebrow_length = 1,
              eyebrow_angle = 1,
              eyebrow_height = 1)

fig, axes = plt.subplots()
ax = cface.plot(axes)
plt.show()
```

## Things to keep in mind
Your responsibilities are to clean your data and filter down to a set of records that you want to compare as Chernoff Faces. The Chernoff Face module is responsible for turning your DataFrame into a Chernoff Faces that you can be plotted on a `matplotlib.axes.Axes`. You are responsible for how to plot those onto a `matplotlib.pyplot.figure`.

Before being used to create a Chernoff Face, your DataFrame must be normalised so each value is within the range 0 to 1 using the `CFace.normalise_df(df)` function, which returns a normalised DataFrame, while maintaining scaling within each column. Only numeric columns are normalised, all non-numeric columns are retained, but skipped for the purposes of Chernoff Face creation.

I recommend that you filter down to a set of records that you want to compare as Chernoff Faces _before_ normalising the DataFrame. Within a given normalised DataFrame, the Chernoff Faces should be comparable, ie. their features should scale with the values themselves. If you normalise the DataFrame before filtering, the normalisation may result in outlier values being overrepresented in the Chernoff Face features. Chernoff Faces from DataFrames that have been normalised separately will _not_ be directly comparable. Chernoff Face visualisation is more suitable for analysis of timeseries and otherwise relatively comparable data.

Internally, a Chernoff Face object stores each feature as a value between 0 and 1. You can manually edit these values, but I'm not sure why you'd want to do that. If you edit the features to ranges outside the range 0 to 1, the face will still draw, but it might look strange.
