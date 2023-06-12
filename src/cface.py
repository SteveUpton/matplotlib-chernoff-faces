import matplotlib

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
    pipil_size = 0.04

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
    right_pupil = matplotlib.patches.Circle([eye_spacing, eye_height], pipil_size)
    right_pupil.set(color='Black')
    left_pupil = matplotlib.patches.Circle([-eye_spacing, eye_height], pipil_size)
    left_pupil.set(color='Black')
    ax.add_artist(right_pupil)
    ax.add_artist(left_pupil)

    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(row.name, loc='left', x=0.02, y=0.02)
    return(ax)

def prep_dataframe(df):
    return df
