import matplotlib.pyplot as plt
import pandas as pd

from cface import CFace

fig, axes = plt.subplots()

cface = CFace(nose_width = 0.5,
              nose_length = 0.5,
              head_width = 0.5,
              head_length = 0.5,
              eye_width = 0.5,
              eye_length = 0.5,
              eye_spacing = 0.5,
              eye_height = 0.5,
              eye_angle = 0.5,
              pupil_size = 0.5,
              mouth_length = 0.5,
              mouth_height = 0.5,
              eyebrow_length = 0.5,
              eyebrow_angle = 0.5,
              eyebrow_height = 0.5)

ax = cface.plot(axes)

plt.show()
