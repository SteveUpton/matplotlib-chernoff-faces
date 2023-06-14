import matplotlib
import math

class CFace():

    defaults = {
        'nose_width': 0.5,
        'nose_length': 0.5,
        'head_width': 0.5,
        'head_length': 0.5,
        'eye_width': 0.5,
        'eye_length': 0.5,
        'eye_spacing': 0.5,
        'eye_height': 0.5,
        'eye_angle': 0.5,
        'pupil_size': 0.5,
        'mouth_length': 0.5,
        'mouth_height': 0.5,
        'eyebrow_length': 0.5,
        'eyebrow_angle': 0.5,
        'eyebrow_height': 0.5
    }

    def __init__(self,
                 nose_width=defaults['nose_width'],
                 nose_length=defaults['nose_length'],
                 head_width=defaults['head_width'],
                 head_length=defaults['head_length'],
                 eye_length=defaults['eye_length'],
                 eye_width=defaults['eye_width'],
                 eye_spacing=defaults['eye_spacing'],
                 eye_height=defaults['eye_height'],
                 eye_angle=defaults['eye_angle'],
                 pupil_size=defaults['pupil_size'],
                 mouth_length=defaults['mouth_length'],
                 mouth_height=defaults['mouth_height'],
                 eyebrow_length=defaults['eyebrow_length'],
                 eyebrow_angle=defaults['eyebrow_angle'],
                 eyebrow_height=defaults['eyebrow_height']):

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
    
    def plot(self, axes=None, name=None):
        ax = axes

        scaled_features = self.features
        for feature, value in self.features.items():
            scaled_features[feature] = value

        # Set axes limits to support absolute drawing
        ax.set_xlim([-1, 1])
        ax.set_ylim([-1, 1])

        # Axes formatting
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(name, loc='left', x=0.02, y=0.02)

        # Draw nose
        nose = matplotlib.patches.Ellipse([0,0], scaled_features['nose_width'], scaled_features['nose_length'])
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
        mouth = matplotlib.patches.Arc([0,scaled_features['mouth_height']], 1, 1, angle=-90-scaled_features['mouth_length']/2, theta1=0, theta2=scaled_features['mouth_length'])
        mouth.set(edgecolor='Black')
        ax.add_artist(mouth)

        return(ax)

def prep_dataframe(df):
    return df
