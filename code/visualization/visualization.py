import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.ticker import MultipleLocator, AutoMinorLocator

from code.classes.grid import Grid
from code.classes.house import House
from code.classes.battery import Battery

grid_size = 50

def visualize(grid: Grid):
    fig, ax = set_up_canvas()

    # random plots
    ax.plot(range(grid_size))
    ax.plot([4, 3, 2, 1])

    # get the grid
    grid = Grid.grid

    # loop through the grid
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if isinstance(cell, House):
                pass
            elif isinstance(cell, Battery):
                pass
    
    # show the plot
    plt.show()

def set_up_canvas():
    # make a figure and an axes cell
    fig, ax = plt.subplots()

    # show grid lines
    ax.grid(visible=True, axis='both', which='major', linewidth=1)
    ax.grid(visible=True, axis='both', which='minor', linewidth=0.5)

    # set limits of grid
    # ax.set_xlim(0, grid_size)
    # ax.set_ylim(0, grid_size)
    
    # Intervals for major x-ticks
    ax.xaxis.set_major_locator(MultipleLocator(10))    
    ax.yaxis.set_major_locator(MultipleLocator(10))

    # Minor ticks : Automatic filling based on the ytick range                                                                                                                                       
    ax.xaxis.set_minor_locator(AutoMinorLocator(10)) 
    ax.yaxis.set_minor_locator(AutoMinorLocator(10)) 

    # add margins
    ax.margins(0.1)

    return (fig, ax)

def load_images():
    house_path = "../../data/images/house.png"
    battery_path = "../../data/images/battery.png"

    house_image = mpimg.imread(house_path)
    battery_image = mpimg.imread(battery_path)

def place_image(x, y, image):
    pass


if __name__ == "__main__":
    visualize()

