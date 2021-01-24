import matplotlib
from matplotlib import pyplot as plt
import numpy as np

cdict = {'red': ((0.0, 0.0, 0.0),
                 (0.1, 0.5, 0.5),
                 (0.2, 0.0, 0.0),
                 (0.4, 0.2, 0.2),
                 (0.6, 0.0, 0.0),
                 (0.8, 1.0, 1.0),
                 (1.0, 1.0, 1.0)),
        'green':((0.0, 0.0, 0.0),
                 (0.1, 0.0, 0.0),
                 (0.2, 0.0, 0.0),
                 (0.4, 1.0, 1.0),
                 (0.6, 1.0, 1.0),
                 (0.8, 1.0, 1.0),
                 (1.0, 0.0, 0.0)),
        'blue': ((0.0, 0.0, 0.0),
                 (0.1, 0.5, 0.5),
                 (0.2, 1.0, 1.0),
                 (0.4, 1.0, 1.0),
                 (0.6, 0.0, 0.0),
                 (0.8, 0.0, 0.0),
                 (1.0, 0.0, 0.0))}

my_cmap = matplotlib.colors.LinearSegmentedColormap('my_colormap',cdict,256)

color_mapping = np.linspace(0, 1, 256)

light_purple = 0.1
dark_purple = 0.07

light_indigo = 0.2
dark_indigo = 0.17

light_blue = 0.4
dark_blue = 0.37

light_green = 0.6
dark_green = 0.7

light_yellow = 0.8
dark_yellow = 0.77

light_orange = 0.85
dark_orange = 0.88

light_red = 0.96
dark_red = 1

no_key = 0


input_array = np.array([np.repeat(light_red, 14),
                        np.repeat(dark_red, 14),
                        np.repeat(light_orange, 14),
                        np.repeat(dark_orange, 14),
                        np.repeat(light_yellow, 14),
                        np.repeat(dark_yellow, 14),
                        np.repeat(light_green, 14),
                        np.repeat(dark_green, 14),
                        np.repeat(light_blue, 14),
                        np.repeat(dark_blue, 14),
                        np.repeat(light_indigo, 14),
                        np.repeat(dark_indigo, 14),
                        np.repeat(light_purple, 14),
                        np.repeat(dark_purple, 14),
                        np.repeat(no_key, 14)])

# input_array = np.random.rand(10,10)

fig = plt.figure()
ax = fig.add_subplot(111)
im = ax.imshow(input_array, cmap=my_cmap, vmin=0, vmax=1)
plt.colorbar(im)
plt.show()