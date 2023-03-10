import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.offsetbox import (OffsetImage, AnnotationBbox)
from matplotlib.ticker import MultipleLocator, AutoMinorLocator
from ..classes.grid import Grid
from ..classes.house import House
from ..classes.battery import Battery


def visualize(grid: Grid) -> None:
    """
    Visualize a smart grid.

    pre : grid is a Grid object
    post: a window should be opened with a plot containing the grid with its
          houses, batteries and cables
    """

    # set up canvas
    fig, ax = set_up_canvas(grid)

    # get and display the batteries
    batteries: list[Battery] = grid.batteries
    display_batteries(ax, batteries)

    # get and display the houses together with their cables
    houses: list[House] = grid.houses
    display_houses_and_cables(ax, houses, batteries)

    # show the plot
    plt.show()


def set_up_canvas(grid: Grid):
    """
    Sets up the 'canvas' to plot upon.

    pre : grid is a Grid object
    post: a tuple with a figure object and axis object is returned
    """

    # make a figure and an axes cell
    fig, ax = plt.subplots()

    # set title
    ax.set_title(f"District {grid.district} with cost {grid.cost}")

    # plot to make sure the entire grid is shown
    ax.plot(range(max(grid.size_grid())), alpha=0)

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
    ax.margins(0.05)

    # set aspect ratio to be square
    ax.set_aspect('equal')

    return (fig, ax)


def display_batteries(ax, batteries: list[Battery]) -> None:
    """
    Places images of batteries on the given ax.

    pre : ax is an Axes object, batteries a list of Battery objects and the
          hardcoded path exists and contains a png of a battery
    post: images of batteries are placed on a grid at the corresponding
          coordinates
    """

    # load battery images
    battery_image_boxes = load_battery_images()

    # loop through batteries and display
    for battery in batteries:
        # choose the correct battery image
        if battery.total_capacity in battery_image_boxes.keys():
            battery_image = battery_image_boxes[battery.total_capacity]
        else:
            battery_image = battery_image_boxes[0]

        # display the battery
        display_battery(ax, battery, battery_image)


def load_battery_images() -> dict[int, OffsetImage]:
    paths = [
        "data/images/battery.png",
        "data/images/Powerstar.png",
        "data/images/Immerse-II.png",
        "data/images/Immerse-III.png",
    ]

    capacities = [
        0,
        450,
        900,
        1800,
    ]

    zooms = [
        0.4,
        0.25,
        0.2,
        0.225,
    ]

    battery_image_boxes = {}

    for i, path in enumerate(paths):
        battery_image_boxes[capacities[i]] = load_imagebox(path, zooms[i])

    return battery_image_boxes


def display_battery(ax, battery: Battery,
                    battery_imagebox: OffsetImage) -> None:
    """
    Display a battery on the given Axes object.

    pre : ax is an Axes object, battery is a Battery object and
          battery_imagebox is an OffsetImage object
    post: the given imagebox is placed on the ax plot at the corresponding
          coordinates
    """

    # get battery coordinates
    x, y = battery.coord_x, battery.coord_y

    # place a battery image on the plot
    place_image(ax, x, y, battery_imagebox)


def display_houses_and_cables(ax, houses: list[House],
                              batteries: list[Battery]) -> None:
    """
    Display the houses and their cables.

    pre : houses is a list of House objects, batteries is a list of Battery
          objects and ax is an Axes object
    post: the houses are displayed on the grid at their corresponding
          coordinates with a house image and for every house their cables are
          plotted
    """

    # load house image
    house_path: str = "data/images/house.png"
    house_imagebox = load_imagebox(house_path, 0.2)

    n_batteries: int = len(batteries)

    # loop through houses and display the house and its cables
    for house in houses:
        display_house(ax, house, house_imagebox)

        if house.connection is not None:
            color_idx = batteries.index(house.connection) / n_batteries
            display_cables(ax, house.cables, color_idx)


def display_house(ax, house: House, house_imagebox: OffsetImage) -> None:
    """
    Display a house on the plot.

    pre : ax is an Axes object, house is a House object and house_imagebox is
          an OffsetImage object
    post: the house is displayed with a house image given by house_imagebox
          at the corresponding coordinates
    """

    # get house coordinates
    x, y = house.coord_x, house.coord_y

    # place a house image on the plot
    place_image(ax, x, y, house_imagebox)


def load_imagebox(path: str, zoom: float) -> OffsetImage:
    """
    Load and create an imagebox.

    pre : path is an existing path and a string, zoom is a float
    post: the imagebox is returned as a OffsetImage object
    """

    image = mpimg.imread(path)

    # The OffsetBox is a simple container artist.
    # The child artists are meant to be drawn at a relative position to its
    # parent.
    imagebox = OffsetImage(image, zoom=zoom)

    return imagebox


def place_image(ax, x: int, y: int, imagebox: OffsetImage):
    """
    Place image on plot.

    pre : ax is an Axes object, x and y are ints and imagebox is an OffsetImage
          object
    post: the image given by imagebox is displayed on the grid at coordinates
          given by x and y
    """

    # Annotation box for image
    # Container for the imagebox referring to a specific position *xy*.
    ab = AnnotationBbox(imagebox, (x, y), frameon=False, zorder=50)
    ax.add_artist(ab)


def display_cables(ax, cable_coordinates: list[str], color_idx: float) -> None:
    """
    Display cables on grid.

    pre : ax is an Axes object, cable_coordinates is a list of strings
          containing the coordinates of the cable and color is a usable color
          for the plot function of pyplot
    post: the cables are plotted at the correct coordinates
    """

    # loop over all elements except the last
    for i in range(len(cable_coordinates) - 1):
        start_x, start_y = get_x_y(cable_coordinates[i])
        end_x, end_y = get_x_y(cable_coordinates[i + 1])

        display_cable(ax, [start_x, end_x], [start_y, end_y], color_idx)


def get_x_y(coordinates: str) -> tuple[int, int]:
    """
    Get the x and y values from a string.

    pre : coordinates is a string and is structured as 'x-value,y-value', which
          are both strings
    post: a tuple of 2 integers x and y is returned
    """

    x, y = coordinates.split(",")
    return (int(x), int(y))


def display_cable(ax, x: list[int], y: list[int], color_idx: float) -> None:
    """
    Display a cable segment.

    pre : ax is an Axes object, x is a list of integers containing the start x
          and then the end x, same goes for y, color should be a usable color for
          the plot function of pyplot
    post: the cable segment is plotted on the ax object with a color depicting
          from which battery it came from
    """
    
    # give the color index a bit of an offset to avoid unclear colors in the
    # colormap
    color_idx += 0.1

    # use the colormap to get an actual color
    color = plt.cm.nipy_spectral(color_idx)

    # calculate the offset of the cable
    offset = (color_idx - 0.5)/20

    # offset x and y coordinates for visibility
    x_offset = [c + offset for c in x]
    y_offset = [c + offset for c in y]

    # plot cable
    ax.plot(x_offset, y_offset, c=color)
