import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.offsetbox import (OffsetImage, AnnotationBbox)
from matplotlib.ticker import MultipleLocator, AutoMinorLocator

from ..classes.grid import Grid
from ..classes.house import House
from ..classes.battery import Battery


grid_size = 50

def visualize(grid: Grid):
    # set up canvas
    fig, ax = set_up_canvas()

    # load the images and make imageboxes
    house_imagebox, battery_imagebox = load_image_boxes()

    # random plots
    ax.plot(range(grid_size), alpha=0)

    # get the grid
    grid = grid.grid

    # loop through the grid
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if isinstance(cell, House):
                place_image(ax, x, y, house_imagebox)
            elif isinstance(cell, Battery):
                place_image(ax, x, y, battery_imagebox)
    
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

def load_image_boxes() -> tuple[OffsetImage, OffsetImage]:
    house_path = "data/images/house.png"
    battery_path = "data/images/battery.png"

    house_image = mpimg.imread(house_path)
    battery_image = mpimg.imread(battery_path)

    #The OffsetBox is a simple container artist.
    #The child artists are meant to be drawn at a relative position to its #parent.
    house_imagebox = OffsetImage(house_image, zoom = 0.2)
    battery_imagebox = OffsetImage(battery_image, zoom = 0.4)

    return (house_imagebox, battery_imagebox)

def place_image(ax, x: int, y: int, image_box: OffsetImage):
    #Annotation box for image
    #Container for the imagebox referring to a specific position *xy*.
    ab = AnnotationBbox(image_box, (x, y), frameon = False)
    ax.add_artist(ab)

def place_dot(ax, x, y, house: bool) -> None:
    if house:
        ax.plot(x, y, 'ro')
    else:
        ax.plot(x, y, 'go')


if __name__ == "__main__":
    visualize()

