
def cface(ax=None, row=None):
    if row is None:
        raise TypeError("Must supply row")
    
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(row.name, loc='left', x=0.02, y=0.02)
    return(ax)

def prep_dataframe(df):
    return df
