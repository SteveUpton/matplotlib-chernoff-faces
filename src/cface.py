import math
import matplotlib
from pandas.api.types import is_numeric_dtype

class CFace():

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
            'default': 0.2
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
    def _scale_feature(value, min, max):
        old_min = 0
        old_range = 1
        new_range = max - min
        return (((value - old_min) * new_range) / old_range) + min

    def plot(self, axes=None, name=None):
        '''
        Plots the Chernoff Face on the supplied axes, with a label set to the supplied name. 

        Parameters:
            axes (axes): The axes on which to plot the face.
            name (str): The label to add to the face.

        Returns:
            ax (axes): The axes containing the plotted face.
        '''
        ax = axes

        # Set axes limits to support absolute drawing
        ax.set_xlim([-1, 1])
        ax.set_ylim([-1, 1])

        # Axes formatting
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(name, loc='left', x=0.02, y=0.02)

        scaled_features = self.features
        for feature, value in self.features.items():
            scaled_features[feature] = CFace._scale_feature(value,
                                                            min=self.feature_ranges[feature]['min'],
                                                            max=self.feature_ranges[feature]['max'])

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
        eyebrow_height_adjusted = scaled_features['eye_height'] + scaled_features['eyebrow_height'] + scaled_features['eye_width']/2 + 0.05
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
    def _normalise_value(value, old_min, old_range):
        if old_range == 0:
            return 1
        return (value - old_min) / old_range

    @staticmethod
    def normalise_df(df):
        normalised_df = df

        feature_list = list(reversed(CFace.feature_ranges.keys()))
        feature_map = {}

        for column_name in normalised_df:
            column = normalised_df[column_name]
            if not is_numeric_dtype(column):
                continue

            old_max = column.max()
            old_min = column.min()
            old_range = old_max - old_min

            normalised_df[column_name] = column.apply(lambda x: CFace._normalise_value(x, old_min, old_range))

            if feature_list:
                feature_map[feature_list.pop()] = column_name

        return normalised_df, feature_map

    @staticmethod
    def _get_feature_from_row(row, feature_name, feature_map):
        if not feature_name in feature_map:
            return CFace.feature_ranges[feature_name]['default']
        return row[feature_map[feature_name]]

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
