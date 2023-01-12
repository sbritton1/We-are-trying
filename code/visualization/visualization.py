import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.offsetbox import (OffsetImage, AnnotationBbox)
from matplotlib.ticker import MultipleLocator, AutoMinorLocator

from ..classes.grid import Grid
from ..classes.house import House
from ..classes.battery import Battery


grid_size = 50

# * TEST STUFF
# grid_lines = ["0,0", "0,1", "1,1", "2,1", "3,1", "4,1", "4,2"]
# grid_lines2 = ["0,0", "0,1", "1,1", "2,1", "2,2", "2,3", "3,3"]

def visualize(grid: Grid):
    # set up canvas
    fig, ax = set_up_canvas()

    # plot to make sure the entire grid is shown
    ax.plot(range(grid_size), alpha=0)

    # get and display the batteries
    batteries = grid.batteries
    display_batteries(ax, batteries)

    # get and display the houses together with their cables
    houses = grid.houses
    display_houses(ax, houses)
    
    # show the plot
    plt.show()

def set_up_canvas():
    # make a figure and an axes cell
    fig, ax = plt.subplots()

    # show grid lines
    ax.grid(visible=True, axis='both', which='major', linewidth=1)
    ax.grid(visible=True, axis='both', which='minor', linewidth=0.5)
    
    # Intervals for major x-ticks
    ax.xaxis.set_major_locator(MultipleLocator(10))    
    ax.yaxis.set_major_locator(MultipleLocator(10))

    # Minor ticks : Automatic filling based on the ytick range                                                                                                                                       
    ax.xaxis.set_minor_locator(AutoMinorLocator(10)) 
    ax.yaxis.set_minor_locator(AutoMinorLocator(10)) 

    # add margins
    ax.margins(0.1)

    return (fig, ax)

def display_batteries(ax, batteries: list[Battery]) -> None:
    # load battery image
    battery_path = "data/images/battery.png"
    battery_imagebox = load_imagebox(battery_path, 0.4)

    # loop through batteries and display
    for battery in batteries:
        display_battery(ax, battery, battery_imagebox)

def display_battery(ax, battery: Battery, battery_imagebox: OffsetImage) -> None:
    # get battery coordinates
    x, y = battery.coord_x, battery.coord_y

    # place a battery image on the plot
    place_image(ax, x, y, battery_imagebox)

def display_houses(ax, houses: list[House]) -> None:
    # load house image
    house_path = "data/images/house.png"
    house_imagebox = load_imagebox(house_path, 0.2)

    # loop through houses and display the house and its cables
    for house in houses:
        display_house(ax, house, house_imagebox)
        display_cables(ax, house.cables)

def display_house(ax, house: House, house_imagebox: OffsetImage) -> None:
    # get house coordinates
    x, y = house.coord_x, house.coord_y

    # place a house image on the plot
    place_image(ax, x, y, house_imagebox)

def load_imagebox(path: str, zoom: float) -> OffsetImage:
    image = mpimg.imread(path)

    #The OffsetBox is a simple container artist.
    #The child artists are meant to be drawn at a relative position to its #parent.
    imagebox = OffsetImage(image, zoom = zoom)

    return imagebox

def place_image(ax, x: int, y: int, imagebox: OffsetImage):
    #Annotation box for image
    #Container for the imagebox referring to a specific position *xy*.
    ab = AnnotationBbox(imagebox, (x, y), frameon = False)
    ax.add_artist(ab)

def place_dot(ax, x, y, house: bool) -> None:
    if house:
        ax.plot(x, y, 'ro')
    else:
        ax.plot(x, y, 'go')

def display_cables(ax, cable_coordinates: list[str]) -> None:
    # loop over all elements except the last
    for i in range(len(cable_coordinates) - 1):
        start_x, start_y = get_x_y(cable_coordinates[i])
        end_x, end_y = get_x_y(cable_coordinates[i + 1])

        display_cable(ax, [start_x, end_x], [start_y, end_y])

def get_x_y(coordinates: str) -> tuple[int, int]:
    x, y = coordinates.split(",")
    return (int(x), int(y))

def display_cable(ax, x: list[int], y: list[int]) -> None:
    ax.plot(x, y, 'b')


if __name__ == "__main__":
    visualize()

