"""
`CFace` provides a class representing a Chernoff Face, with instance methods for plotting the
face to a supplied `Axes`. Static helper methods allow for the normalisation of a `pandas.DataFrame`
to prepare it for use in Chernoff Face creation, and the creation of a Chernoff Face when supplied
with a row from a normalised DataFrame.

The suggested workflow is:

    import matplotlib.pyplot as plt
    import pandas as pd

    from cface import CFace

    df = pd.read_csv('data.csv')
    df = df_satcat.set_index('Name')

    # Clean and filter the data you want to visualise as Chernoff Faces

    # Normalise the dataframe to prepare for Chernoff Face creation
    df_faces, feature_map = CFace.normalise_df(df)

    # If you want to change the mapping from features to columns, now is the time

    # Create Chernoff Faces for each row of the DataFrame
    df_faces['cface'] = df_faces.apply(CFace.create_cface_from_row, axis=1, feature_map=feature_map)

    # Visualise the Chernoff faces (this example assumes 20 rows in df_faces and a Name column)
    fig = plt.figure(figsize=(10,8))
    for i in range(len(df_faces)):
        ax = fig.add_subplot(4, 5, i+1, aspect='equal')
        df_faces.iloc[i, df_faces.columns.get_loc("cface")].plot(ax, df_faces.iloc[i]['Name'])

    plt.show()

You can also create a Chernoff Face directly

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

Your responsibilities are to clean your data and filter down to a set of records that you want to compare
as Chernoff Faces. The Chernoff Face module is responsible for turning your DataFrame into a set of Chernoff
Faces that you can visualise on `matplotlib.axes.Axes`. You are responsible for how to visualise that onto
a `matplotlib.pyplot.figure`.
"""
import math
import matplotlib
from pandas.api.types import is_numeric_dtype

class CFace():
    '''
    A Chernoff Face with instance methods for plotting the face to a supplied `Axes`. Static
    helper methods allow for the normalisation of a `pandas.DataFrame` to prepare it for use in Chernoff
    Face creation, and the creation of a Chernoff Face when supplied with a row from a normalised DataFrame.

    The features of the Chernoff Face are stored in an instance variable `features`, a dict with the
    following keys:  
    nose_width : The width of the nose.
    nose_length : The length of the nose.
    head_width : The width of the head.
    head_length : The length of the head.
    eye_width : The width of the eyes.
    eye_length : The length of the eyes.
    eye_spacing : How distance between the eyes.
    eye_height : How far above the center of the face the eyes are drawn. 
    eye_angle : The angle of the eyes.
    pupil_size : The size of the pupils.
    mouth_length : The length (width) of the mouth.
    mouth_height : How far below the center of the face the mouth is drawn.
    eyebrow_length : The length of the eyebrows.
    eyebrow_angle : The angle of the eyebrows.
    eyebrow_height : How high the eyebrows are drawn, relative to the eyes.

    All features are stored as floats and should be in the range 0-1. You can manually adjust the
    features to values outside this range, but the behaviour is undefined (the face is likely to
    look weird.)
    '''

    feature_ranges = {
        'nose_width': {
            'min': 0.01,
            'max': 0.10,
            'default': 0.5
        },
        'nose_length': {
            'min': 0.10,
            'max': 0.50,
            'default': 0.5
        },
        'head_width': {
            'min': 0.80,
            'max': 2,
            'default': 0.5
        },
        'head_length': {
            'min': 0.80,
            'max': 2,
            'default': 0.5
        },
        'eye_width': {
            'min': 0.10,
            'max': 0.30,
            'default': 0.5
        },
        'eye_length': {
            'min': 0.10,
            'max': 0.35,
            'default': 0.5
        },
        'eye_spacing': {
            'min': 0.05,
            'max': 0.35,
            'default': 0.5
        },
        'eye_height': {
            'min': 0.1,
            'max': 0.3,
            'default': 0.5
        },
        'eye_angle': {
            'min': 70.00,
            'max': 110,
            'default': 0.5
        },
        'pupil_size': {
            'min': 0.01,
            'max': 0.07,
            'default': 0.5
        },
        'mouth_length': {
            'min': 10,
            'max': 100,
            'default': 0.5
        },
        'mouth_height': {
            'min': 0.01,
            'max': 0.5,
            'default': 0.5
        },
        'eyebrow_length': {
            'min': 0.10,
            'max': 0.30,
            'default': 0.5
        },
        'eyebrow_angle': {
            'min': -20.00,
            'max': 20.0,
            'default': 0.5
        },
        'eyebrow_height': {
            'min': 0.00,
            'max': 0.15,
            'default': 0.5
        }
    }

    def __init__(self,
                 nose_width=feature_ranges['nose_width']['default'],
                 nose_length=feature_ranges['nose_length']['default'],
                 head_width=feature_ranges['head_width']['default'],
                 head_length=feature_ranges['head_length']['default'],
                 eye_length=feature_ranges['eye_length']['default'],
                 eye_width=feature_ranges['eye_width']['default'],
                 eye_spacing=feature_ranges['eye_spacing']['default'],
                 eye_height=feature_ranges['eye_height']['default'],
                 eye_angle=feature_ranges['eye_angle']['default'],
                 pupil_size=feature_ranges['pupil_size']['default'],
                 mouth_length=feature_ranges['mouth_length']['default'],
                 mouth_height=feature_ranges['mouth_height']['default'],
                 eyebrow_length=feature_ranges['eyebrow_length']['default'],
                 eyebrow_angle=feature_ranges['eyebrow_angle']['default'],
                 eyebrow_height=feature_ranges['eyebrow_height']['default']):
        '''
        Parameters:
            nose_width (float) : default: 0.5, range: (0-1)
                The width of the nose.
            nose_length (float) : default: 0.5, range: (0-1)
                The length of the nose.
            head_width (float) : default: 0.5, range: (0-1)
                The width of the head.
            head_length (float) : default: 0.5, range: (0-1)
                The length of the head.
            eye_width (float) : default: 0.5, range: (0-1)
                The width of the eyes.
            eye_length (float) : default: 0.5, range: (0-1)
                The length of the eyes.
            eye_spacing (float) : default: 0.5, range: (0-1)
                How distance between the eyes.
            eye_height (float) : default: 0.5, range: (0-1)
                How far above the center of the face the eyes are drawn. 
            eye_angle (float) : default: 0.5, range: (0-1)
                The angle of the eyes.
            pupil_size (float) : default: 0.5, range: (0-1)
                The size of the pupils.
            mouth_length (float) : default: 0.5, range: (0-1)
                The length (width) of the mouth.
            mouth_height (float) : default: 0.5, range: (0-1)
                How far below the center of the face the mouth is drawn.
            eyebrow_length (float) : default: 0.5, range: (0-1)
                The length of the eyebrows.
            eyebrow_angle (float) : default: 0.5, range: (0-1)
                The angle of the eyebrows.
            eyebrow_height (float) : default: 0.5, range: (0-1)
                How high the eyebrows are drawn, relative to the eyes.
        '''

        self.features = {
            'nose_width': nose_width,
            'nose_length': nose_length,
            'head_width': head_width,
            'head_length': head_length,
            'eye_width': eye_width,
            'eye_length': eye_length,
            'eye_spacing': eye_spacing,
            'eye_height': eye_height,
            'eye_angle': eye_angle,
            'pupil_size': pupil_size,
            'mouth_length': mouth_length,
            'mouth_height': mouth_height,
            'eyebrow_length': eyebrow_length,
            'eyebrow_angle': eyebrow_angle,
            'eyebrow_height': eyebrow_height
        }

        for feature, value in self.features.items():
            if value > 1 or value < 0:
                raise ValueError(f'{feature} value {value} must be within the range 0 to 1')

    @staticmethod
    def normalise_df(df):
        '''
        Normalises a `pandas.DataFrame` and returns a mapping between Chernoff Face features and
        and column names in the normalised DataFrame.
        
        Takes a `pandas.DataFrame` and returns a copy of that DataFrame, with numeric values
        normalised to a range from 0 to 1, maintaining per column scaling. Non numeric or mixed type
        columns will not be normalised or appear in the feature_map.

        Also returns feature_map, a dict with the keys being Chernoff Face features and values being
        column names in the DataFrame. If there are more features than normalised columns, then feature_map
        will only contain feature to column name mappings up to the number of columns. If there are more
        normalised columns than features, then feature_map will only contain mappings to the first
        columns that were normalised.

        All columns that can be normalised will be normalised, allowing you to edit feature_map to
        adjust the mappings manually. Multiple features can be mapped to the same column name. A complete
        feature_map looks like this:

        ```
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

        Parameters:
            df (`pandas.DataFrame`): A DataFrame of data to be normalised.

        Returns:
            df (`pandas.DataFrame`): A normalised DataFrame.
            feature_map (dict): A mapping between Chernoff Face features and columns in the DataFrame.
        '''
        normalised_df = df.copy()

        feature_list = list(reversed(CFace.feature_ranges.keys()))
        feature_map = {}

        for column_name in normalised_df:
            column = normalised_df[column_name]

            # If the column is not numeric, ignore it
            if not is_numeric_dtype(column):
                continue

            #  Normalise the column, according to the range of the column
            old_max = column.max()
            old_min = column.min()
            old_range = old_max - old_min

            normalised_df[column_name] = column.apply(lambda x: CFace._normalise_value(x, old_min, old_range))

            # Map the normalised column to the next available feature
            if feature_list:
                feature_map[feature_list.pop()] = column_name

        return normalised_df, feature_map

    @staticmethod
    def create_cface_from_row(row, feature_map):
        '''
        Creates a Chernoff Face based on a (normalised) dataframe row and a feature map defining
        the mapping between features (of the Chernoff Face) and columns (of the supplied dataframe).         

        Parameters:
            row (pandas.Series): A normalised row.
            feature_map (dict): A mapping between features and column names.

        Returns:
            `CFace`: The Chernoff Face
        '''
        return CFace(nose_width = CFace._get_feature_from_row(row, 'nose_width', feature_map),
                     nose_length = CFace._get_feature_from_row(row, 'nose_length', feature_map),
                     head_width = CFace._get_feature_from_row(row, 'head_width', feature_map),
                     head_length = CFace._get_feature_from_row(row, 'head_length', feature_map),
                     eye_width = CFace._get_feature_from_row(row, 'eye_width', feature_map),
                     eye_length = CFace._get_feature_from_row(row, 'eye_length', feature_map),
                     eye_spacing = CFace._get_feature_from_row(row, 'eye_spacing', feature_map),
                     eye_height = CFace._get_feature_from_row(row, 'eye_height', feature_map),
                     eye_angle = CFace._get_feature_from_row(row, 'eye_angle', feature_map),
                     pupil_size = CFace._get_feature_from_row(row, 'pupil_size', feature_map),
                     mouth_length = CFace._get_feature_from_row(row, 'mouth_length', feature_map),
                     mouth_height = CFace._get_feature_from_row(row, 'mouth_height', feature_map),
                     eyebrow_length = CFace._get_feature_from_row(row, 'eyebrow_length', feature_map),
                     eyebrow_angle = CFace._get_feature_from_row(row, 'eyebrow_angle', feature_map),
                     eyebrow_height = CFace._get_feature_from_row(row, 'eyebrow_height', feature_map))


    def plot(self, ax=None, name=None):
        '''
        Plots the Chernoff Face on the supplied axes, with a label set to the supplied name. 

        Parameters:
            axes (axes): The axes on which to plot the face.
            name (str): The label to add to the face.

        Returns:
            ax (axes): The axes containing the plotted face.
        '''
        # Set axes limits to support absolute drawing
        ax.set_xlim([-1, 1])
        ax.set_ylim([-1, 1])

        # Axes formatting
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(name, loc='left', x=0.02, y=0.02)

        # Scale features to appropriate, per feature ranges
        scaled_features = self.features.copy()
        for feature, value in self.features.items():
            scaled_features[feature] = CFace._scale_feature(value,
                                                            new_min=self.feature_ranges[feature]['min'],
                                                            new_max=self.feature_ranges[feature]['max'])

        # Draw nose
        nose = matplotlib.patches.Ellipse(xy=[0,0+scaled_features['nose_length']/4],
                                          width=scaled_features['nose_width'],
                                          height=scaled_features['nose_length'])
        nose.set(edgecolor='Black', fill=False)
        ax.add_artist(nose)

        # Draw head
        head = matplotlib.patches.Ellipse(xy=[0,0],
                                          width=scaled_features['head_width'],
                                          height=scaled_features['head_length'])
        head.set(edgecolor='Black', fill=False)
        ax.add_artist(head)

        # Draw eyes
        right_eye = matplotlib.patches.Ellipse(xy=[scaled_features['eye_spacing'], scaled_features['eye_height']],
                                               width=scaled_features['eye_width'],
                                               height=scaled_features['eye_length'],
                                               angle=scaled_features['eye_angle'])
        right_eye.set(edgecolor='Black', fill=False)
        left_eye = matplotlib.patches.Ellipse(xy=[-scaled_features['eye_spacing'], scaled_features['eye_height']],
                                              width=scaled_features['eye_width'],
                                              height=scaled_features['eye_length'],
                                              angle=-scaled_features['eye_angle'])
        left_eye.set(edgecolor='Black', fill=False)
        ax.add_artist(right_eye)
        ax.add_artist(left_eye)

        # Draw pupils
        right_pupil = matplotlib.patches.Circle(xy=[scaled_features['eye_spacing'], scaled_features['eye_height']],
                                                radius=scaled_features['pupil_size'])
        right_pupil.set(color='Black')
        left_pupil = matplotlib.patches.Circle(xy=[-scaled_features['eye_spacing'], scaled_features['eye_height']],
                                               radius=scaled_features['pupil_size'])
        left_pupil.set(color='Black')
        ax.add_artist(right_pupil)
        ax.add_artist(left_pupil)

        # Draw eyebrows
        eyebrow_opp = math.sin(math.radians(scaled_features['eyebrow_angle'])) * scaled_features['eyebrow_length']
        eyebrow_adj = math.cos(math.radians(scaled_features['eyebrow_angle'])) * scaled_features['eyebrow_length']
        eyebrow_spacing = scaled_features['eye_spacing'] - scaled_features['eyebrow_length']/2
        eyebrow_height_adjusted = (scaled_features['eye_height'] + scaled_features['eyebrow_height'] +
                                   scaled_features['eye_width']/2 + 0.05)
        right_eyebrow = matplotlib.lines.Line2D(xdata=[eyebrow_spacing, eyebrow_spacing+eyebrow_adj],
                                                ydata=[eyebrow_height_adjusted, eyebrow_height_adjusted+eyebrow_opp])
        right_eyebrow.set(color='Black')
        left_eyebrow = matplotlib.lines.Line2D(xdata=[-eyebrow_spacing, -eyebrow_spacing-eyebrow_adj],
                                               ydata=[eyebrow_height_adjusted, eyebrow_height_adjusted+eyebrow_opp])
        left_eyebrow.set(color='Black')
        ax.add_artist(left_eyebrow)
        ax.add_artist(right_eyebrow)

        # Draw mouth
        mouth_distance_from_center = min((scaled_features['mouth_height']),
                                         (scaled_features['head_length']/2 - scaled_features['head_length']/6))
        mouth = matplotlib.patches.Arc(xy=[0,-mouth_distance_from_center+0.01],
                                       width=scaled_features['head_length']/3,
                                       height=scaled_features['head_length']/3,
                                       angle=-90-scaled_features['mouth_length']/2,
                                       theta1=0,
                                       theta2=scaled_features['mouth_length'])
        mouth.set(edgecolor='Black')
        ax.add_artist(mouth)

        return ax

    @staticmethod
    def _scale_feature(value, new_min, new_max):
        '''
        Takes a value in the range 0 to 1 and scales it to the new range, defined by new_min and new_max.

        Parameters:
            value (float): The value to be scaled.
            new_min (float): The minimum of the new range.
            new_max (float): The maximum of the new range.

        Returns:
            float
        '''
        old_min = 0
        old_range = 1
        new_range = new_max - new_min
        return (((value - old_min) * new_range) / old_range) + new_min

    @staticmethod
    def _normalise_value(value, old_min, old_range):
        '''
        Takes a value from a set of values (column) with a specified range and normalises that value to
        the range 0 to 1, retaining scaling of the value within it's original range.

        Parameters:
            value (float): The value to be scaled.
            old_min (float): The minimum of the old range.
            old_max (float): The maximum of the old range.

        Returns:
            float
        '''
        if old_range == 0:
            return 1
        return (value - old_min) / old_range

    @staticmethod
    def _get_feature_from_row(row, feature_name, feature_map):
        '''
        Given a row (`pandas.Series`), extracts the value for `feature_name` from the appropriate column
        as described by the mapping in `feature_map`.

        If `feature_name` is not present in the `feature_map`, then the default value for that feature
        is returned.

        Parameters:
            row (`pandas.Series`): The row from which to extract the feature.
            feature_name (str): The name of the feature to extract.
            feature_map (dict): A mapping between Chernoff Face features and columns in the DataFrame.

        Returns:
            float
        '''
        if not feature_name in feature_map:
            return CFace.feature_ranges[feature_name]['default']
        return row[feature_map[feature_name]]
