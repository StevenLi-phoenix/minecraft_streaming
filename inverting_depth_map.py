import matplotlib.pyplot as plt
import numpy as np

img1_path = "new_york_deep_ets/new-york-statue-of-liberty_16x9_M.png"
img2_path = "new_york_deep_ets/new-york-statue-of-liberty_16x9_L.png"
img1 = plt.imread(img1_path)
img2 = plt.imread(img2_path)

# reverse prediction
img2 = np.ones(np.shape(img2)) - img2

"""
img1_max = np.max(img1)
img1_min = np.min(img1)
img2_max = np.max(img2)
img2_min = np.min(img2)
img2 = (img2 - img2_min) / (img2_max - img2_min) * (img1_max - img1_min) + img1_min
"""

fig, ax = plt.subplots(nrows=2, ncols=2)
ax[0,0].imshow(img1)
ax[0,1].imshow(img2)
ax[1,0].hist(img1.flatten())
ax[1,1].hist(img2.flatten())
fig.show()