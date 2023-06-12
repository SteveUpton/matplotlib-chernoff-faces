import matplotlib

def cface(ax=None, row=None):
    if row is None:
        raise TypeError("Must supply row")
    
    # Set axes limits to support absolute drawing
    ax.set_xlim([-1, 1])
    ax.set_ylim([-1, 1])

    nose_width = 0.1    # Max
    nose_length = 0.5   # Max

    # Draw nose
    nose = matplotlib.patches.Ellipse([0,0], nose_width, nose_length)
    nose.set(edgecolor='Black', fill=False)
    ax.add_artist(nose)

    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(row.name, loc='left', x=0.02, y=0.02)
    return(ax)

def prep_dataframe(df):
    return df
