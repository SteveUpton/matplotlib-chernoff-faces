import matplotlib.pyplot as plt
import pandas as pd

from cface import cface

fig, axes = plt.subplots()

df = pd.DataFrame([[0, 0], [1, 1], [2, 2]], columns=['A', 'B'])

row = df.iloc[1]
cface(ax=axes, row=row)
plt.show()
