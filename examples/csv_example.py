import matplotlib.pyplot as plt
import pandas as pd

import sys
sys.path.insert(1, '../src')
from cface import CFace

# Import your data
df = pd.read_csv('data.csv')

# Normalise the DataFrame to prepare for Chernoff Face creation
df_faces, feature_map = CFace.normalise_df(df)

# Create a Chernoff Face for each row of the DataFrame
df_faces['cface'] = df_faces.apply(CFace.create_cface_from_row, axis=1, feature_map=feature_map)

# Visualise the Chernoff Faces (this example assumes 20 rows in df_faces)
fig = plt.figure(figsize=(20,16))
for i in range(len(df_faces)):
    ax = fig.add_subplot(4, 5, i+1, aspect='equal')
    df_faces.iloc[i, df_faces.columns.get_loc("cface")].plot(ax, i)

fig.subplots_adjust(hspace=0, wspace=0)

plt.savefig('20_faces.png', bbox_inches='tight')
