import matplotlib.pyplot as plt
import pandas as pd

import sys
sys.path.insert(1, '../src')
from cface import CFace

cface_default = CFace()

cface_max = CFace(nose_width = 1,
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

cface_min = CFace(nose_width = 0,
                  nose_length = 0,
                  head_width = 0,
                  head_length = 0,
                  eye_width = 0,
                  eye_length = 0,
                  eye_spacing = 0,
                  eye_height = 0,
                  eye_angle = 0,
                  pupil_size = 0,
                  mouth_length = 0,
                  mouth_height = 0,
                  eyebrow_length = 0,
                  eyebrow_angle = 0,
                  eyebrow_height = 0)

df = pd.DataFrame([cface_min, cface_default, cface_max],
                  columns=['cface'],
                  index=['min', 'default', 'max'])

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

for i in range(len(df)):
    df.iloc[i, df.columns.get_loc("cface")].plot(axes[i], df.iloc[i].name)

fig.subplots_adjust(hspace=0, wspace=0)

plt.savefig('faces.png', bbox_inches='tight')
