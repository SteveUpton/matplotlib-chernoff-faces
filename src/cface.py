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

        self._validate_feature_ranges()

    def _validate_feature_ranges(self):
        for feature, value in self.features.items():
            if value > 1 or value < 0:
                raise ValueError('{} value {} must be within the range 0 to 1'.format(feature, value))
        return
    
    def _scale_feature(value, min, max):
        old_min = 0
        old_range = 1
        new_range = max - min
        return (((value - old_min) * new_range) / old_range) + min

    def plot(self, axes=None, name=None):
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
        nose = matplotlib.patches.Ellipse([0,0+scaled_features['nose_length']/4], scaled_features['nose_width'], scaled_features['nose_length'])
        nose.set(edgecolor='Black', fill=False)
        ax.add_artist(nose)

        # Draw head
        head = matplotlib.patches.Ellipse([0,0], scaled_features['head_width'], scaled_features['head_length'])
        head.set(edgecolor='Black', fill=False)
        ax.add_artist(head)

        # Draw eyes
        right_eye = matplotlib.patches.Ellipse([scaled_features['eye_spacing'], scaled_features['eye_height']], scaled_features['eye_width'], scaled_features['eye_length'], angle=scaled_features['eye_angle'])
        right_eye.set(edgecolor='Black', fill=False)
        left_eye = matplotlib.patches.Ellipse([-scaled_features['eye_spacing'], scaled_features['eye_height']], scaled_features['eye_width'], scaled_features['eye_length'], angle=-scaled_features['eye_angle'])
        left_eye.set(edgecolor='Black', fill=False)
        ax.add_artist(right_eye)
        ax.add_artist(left_eye)

        # Draw pupils
        right_pupil = matplotlib.patches.Circle([scaled_features['eye_spacing'], scaled_features['eye_height']], scaled_features['pupil_size'])
        right_pupil.set(color='Black')
        left_pupil = matplotlib.patches.Circle([-scaled_features['eye_spacing'], scaled_features['eye_height']], scaled_features['pupil_size'])
        left_pupil.set(color='Black')
        ax.add_artist(right_pupil)
        ax.add_artist(left_pupil)

        # Draw eyebrows
        eyebrow_opp = math.sin(math.radians(scaled_features['eyebrow_angle'])) * scaled_features['eyebrow_length']
        eyebrow_adj = math.cos(math.radians(scaled_features['eyebrow_angle'])) * scaled_features['eyebrow_length']
        eyebrow_spacing = scaled_features['eye_spacing'] - scaled_features['eyebrow_length']/2
        eyebrow_height_adjusted = scaled_features['eye_height'] + scaled_features['eyebrow_height'] + scaled_features['eye_width']/2 + 0.05
        right_eyebrow = matplotlib.lines.Line2D([eyebrow_spacing, eyebrow_spacing+eyebrow_adj], [eyebrow_height_adjusted, eyebrow_height_adjusted+eyebrow_opp])
        right_eyebrow.set(color='Black')
        left_eyebrow = matplotlib.lines.Line2D([-eyebrow_spacing, -eyebrow_spacing-eyebrow_adj], [eyebrow_height_adjusted, eyebrow_height_adjusted+eyebrow_opp])
        left_eyebrow.set(color='Black')
        ax.add_artist(left_eyebrow)
        ax.add_artist(right_eyebrow)

        # Draw mouth
        mouth_distance_from_center = min((scaled_features['mouth_height']), (scaled_features['head_length']/2 - scaled_features['head_length']/6))
        mouth = matplotlib.patches.Arc([0,-mouth_distance_from_center+0.01], scaled_features['head_length']/3, scaled_features['head_length']/3, angle=-90-scaled_features['mouth_length']/2, theta1=0, theta2=scaled_features['mouth_length'])
        mouth.set(edgecolor='Black')
        ax.add_artist(mouth)

        return ax

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

            def scale(value, old_min, old_range):
                if old_range == 0:
                    return 1
                else:
                    return (((value - old_min)) / old_range)

            normalised_df[column_name] = column.apply(lambda x: scale(x, old_min, old_range))

            if feature_list:
                feature_map[feature_list.pop()] = column_name

        return normalised_df, feature_map

    def create_cface_from_row(row, feature_map):

        def get_feature(row, feature_name):
            if not feature_name in feature_map:
                return CFace.feature_ranges[feature_name]['default']
            else:
                return row[feature_map[feature_name]]

        return CFace(nose_width = get_feature(row, 'nose_width'),
                     nose_length = get_feature(row, 'nose_length'),
                     head_width = get_feature(row, 'head_width'),
                     head_length = get_feature(row, 'head_length'),
                     eye_width = get_feature(row, 'eye_width'),
                     eye_length = get_feature(row, 'eye_length'),
                     eye_spacing = get_feature(row, 'eye_spacing'),
                     eye_height = get_feature(row, 'eye_height'),
                     eye_angle = get_feature(row, 'eye_angle'),
                     pupil_size = get_feature(row, 'pupil_size'),
                     mouth_length = get_feature(row, 'mouth_length'),
                     mouth_height = get_feature(row, 'mouth_height'),
                     eyebrow_length = get_feature(row, 'eyebrow_length'),
                     eyebrow_angle = get_feature(row, 'eyebrow_angle'),
                     eyebrow_height = get_feature(row, 'eyebrow_height'))
