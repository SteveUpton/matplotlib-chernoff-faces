
def cface(ax=None, row=None):
    if row is None:
        raise TypeError("Must supply row")
    
    ax.set_xticks([])
    ax.set_yticks([])
    return(ax)

def prep_dataframe(df):
    return df
