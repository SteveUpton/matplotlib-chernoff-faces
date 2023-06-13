import matplotlib
import math

def cface(ax=None, row=None):
    if row is None:
        raise TypeError("Must supply row")
    
    # Set axes limits to support absolute drawing
    ax.set_xlim([-1, 1])
    ax.set_ylim([-1, 1])

    nose_width = 0.1    # Max
    nose_length = 0.5   # Max
    head_width = 1.3    # Max
    head_length = 1.5   # Max
    eye_width = 0.2
    eye_length = 0.3
    eye_spacing = 0.25
    eye_height = 0.2
    eye_angle = 110
    pupil_size = 0.04
    mouth_length = 30
    mouth_height = 0.1
    eyebrow_length = 0.2
    eyebrow_angle = 30
    eyebrow_height = 0.1

    # Draw nose
    nose = matplotlib.patches.Ellipse([0,0], nose_width, nose_length)
    nose.set(edgecolor='Black', fill=False)
    ax.add_artist(nose)

    # Draw head
    head = matplotlib.patches.Ellipse([0,0], head_width, head_length)
    head.set(edgecolor='Black', fill=False)
    ax.add_artist(head)

    # Draw eyes
    right_eye = matplotlib.patches.Ellipse([eye_spacing, eye_height], eye_width, eye_length, angle=eye_angle)
    right_eye.set(edgecolor='Black', fill=False)
    left_eye = matplotlib.patches.Ellipse([-eye_spacing, eye_height], eye_width, eye_length, angle=-eye_angle)
    left_eye.set(edgecolor='Black', fill=False)
    ax.add_artist(right_eye)
    ax.add_artist(left_eye)

    # Draw pupils
    right_pupil = matplotlib.patches.Circle([eye_spacing, eye_height], pupil_size)
    right_pupil.set(color='Black')
    left_pupil = matplotlib.patches.Circle([-eye_spacing, eye_height], pupil_size)
    left_pupil.set(color='Black')
    ax.add_artist(right_pupil)
    ax.add_artist(left_pupil)

    # Draw eyebrows
    eyebrow_opp = math.sin(math.radians(eyebrow_angle)) * eyebrow_length
    eyebrow_adj = math.cos(math.radians(eyebrow_angle)) * eyebrow_length
    eyebrow_spacing = eye_spacing - eyebrow_length/2
    eyebrow_height_adjusted = eye_height + eyebrow_height + eye_width/2 + 0.05
    right_eyebrow = matplotlib.lines.Line2D([eyebrow_spacing, eyebrow_spacing+eyebrow_adj], [eyebrow_height_adjusted, eyebrow_height_adjusted+eyebrow_opp])
    right_eyebrow.set(color='Black')
    left_eyebrow = matplotlib.lines.Line2D([-eyebrow_spacing, -eyebrow_spacing-eyebrow_adj], [eyebrow_height_adjusted, eyebrow_height_adjusted+eyebrow_opp])
    left_eyebrow.set(color='Black')
    ax.add_artist(left_eyebrow)
    ax.add_artist(right_eyebrow)

    # Draw mouth
    mouth = matplotlib.patches.Arc([0,mouth_height], 1, 1, angle=-90-mouth_length/2, theta1=0, theta2=mouth_length)
    mouth.set(edgecolor='Black')
    ax.add_artist(mouth)

    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(row.name, loc='left', x=0.02, y=0.02)
    return(ax)

def prep_dataframe(df):
    return df
