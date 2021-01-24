from colour import Color
from matplotlib.colors import LinearSegmentedColormap
from matplotlib import pyplot as plt
import numpy as np


light_rose = '#FF00B2'
dark_rose = '#CC008F'
light_rose_code = 0.0
dark_rose_code = 0.05

light_magenta = '#FF00FF'
dark_magenta = '#FF00FF'
light_magenta_code = 0.11
dark_magenta_code = 0.14

light_violet = '#7B00FF'
dark_violet = '#6300CC'
light_violet_code = 0.17
dark_violet_code = 0.2

light_blue = '#0000FF'
dark_blue = '#0000CC'
light_blue_code = 0.32
dark_blue_code = 0.3

light_azure = '#0055FF'
dark_azure = '#0044CC'
light_azure_code = 0.39
dark_azure_code = 0.38

light_cyan = '#00FFFF'
dark_cyan = '#00CCCC'
light_cyan_code = 0.42
dark_cyan_code = 0.45

light_spring = '#00FF88'
dark_spring = '#00CC6D'
light_spring_code = 0.5
dark_spring_code = 0.53

light_green = '#00FF00'
dark_green = '#00CC00'
light_green_code = 0.6
dark_green_code = 0.62

light_chartreuse = '#6EFF00'
dark_chartreuse = '#58CC00'
light_chartreuse_code = 0.70
dark_chartreuse_code = 0.72

light_yellow = '#FFFF00'
dark_yellow = '#CCCC00'
light_yellow_code = 0.75
dark_yellow_code = 0.78

light_orange = '#FF9100'
dark_orange = '#E68200'
light_orange_code = 0.83
dark_orange_code = 0.87

light_red = '#FF0000'
dark_red = '#CC0000'
light_red_code = 0.92
dark_red_code = 0.95

black = '#000000'
black_code = 1.0

ramp_colors = [light_rose, dark_rose, light_magenta, dark_magenta, light_violet, dark_violet, light_blue, dark_blue,
               light_azure, dark_azure, light_cyan, dark_cyan, light_spring, dark_spring, light_green, dark_green,
               light_chartreuse, dark_chartreuse, light_yellow, dark_yellow, light_orange, dark_orange, light_red,
               dark_red, black]

my_cmap = LinearSegmentedColormap.from_list( 'my_cmap', [Color(color).rgb for color in ramp_colors])

# input_array = np.random.rand(10,10)

input_array = np.array([np.repeat(light_rose_code, 25),
                        np.repeat(dark_rose_code, 25),
                        np.repeat(light_magenta_code, 25),
                        np.repeat(dark_magenta_code, 25),
                        np.repeat(light_violet_code, 25),
                        np.repeat(dark_violet_code, 25),
                        np.repeat(light_blue_code, 25),
                        np.repeat(dark_blue_code, 25),
                        np.repeat(light_azure_code, 25),
                        np.repeat(dark_azure_code, 25),
                        np.repeat(light_cyan_code, 25),
                        np.repeat(dark_cyan_code, 25),
                        np.repeat(light_spring_code, 25),
                        np.repeat(dark_spring_code, 25),
                        np.repeat(light_green_code, 25),
                        np.repeat(dark_green_code, 25),
                        np.repeat(light_chartreuse_code, 25),
                        np.repeat(dark_chartreuse_code, 25),
                        np.repeat(light_yellow_code, 25),
                        np.repeat(dark_yellow_code, 25),
                        np.repeat(light_orange_code, 25),
                        np.repeat(dark_orange_code, 25),
                        np.repeat(light_red_code, 25),
                        np.repeat(dark_red_code, 25),
                        np.repeat(black_code, 25)])

fig = plt.figure()
ax = fig.add_subplot(111)
im = ax.imshow(input_array, cmap=my_cmap, vmin=0, vmax=1)
plt.colorbar(im)
plt.show()