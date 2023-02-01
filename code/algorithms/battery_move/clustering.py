from random import randint
from random import choice

from ...classes.grid import Grid
from ...classes.battery import Battery
from ..own_cables.greedy import greedy


def clustering(grid: Grid, connect: bool = True) -> Grid:
    """"
    Clusters the batteries on a grid according to the houses using K-means
    clustering.

    Pre : grid is a Grid object with no connections and no cables
    Post: the batteries are clustered and connections are made using the greedy
          algorithm, the grid is then returned
    """

    # * ALGORITHM PARAMETERS
    n_iterations = 10

    # randomly place batteries
    random_place_batteries(grid)

    for _ in range(n_iterations):
        # connect each house to the closest battery (without load)
        connect_closest_houses(grid)

        # move the battery to the center of its connected houses
        move_batteries_to_center(grid)

        # remove all connections
        grid.remove_all_connections()

    print("Clustering complete!")

    if connect:
        # perform the connection algorithm
        print("Running connection algorithm...")
        grid = greedy(grid)

    return grid


def random_place_batteries(grid: Grid) -> None:
    """
    Randomly place the batteries on the given grid.

    Pre : grid is a Grid object
    Post: the given grid is modified such that the batteries are placed
          randomly, but not on top of a house or other battery
    """

    # get the maximum range of coordinates
    max_x, max_y = grid.max_x, grid.max_y

    # go over each battery and move it randomly
    for battery in grid.batteries:
        random_x, random_y = get_random_coordinates(max_x, max_y)

        # move untill move_battery returns True and thus is succesful
        while grid.move_battery(battery, random_x, random_y) is False:
            # if move was not succesful, get new random coordinates
            random_x, random_y = get_random_coordinates(max_x, max_y)


def get_random_coordinates(max_x: int, max_y: int) -> tuple[int, int]:
    """
    Get a random coordinate in the given range.

    Pre : max_x and max_y are positive integers
    Post: a tuple is returned as such (random x, random y) both in given range
    """

    return (randint(0, max_x), randint(0, max_y))


def connect_closest_houses(grid: Grid) -> None:
    """
    Connects all houses to the closest battery without loading it.

    Pre : grid is a Grid object with no connections
    Post: every house is connected to the closest battery without adjusting
          the capacity of the battery
    """

    # get the batteries and houses of the grid
    batteries = grid.batteries
    houses = grid.houses

    for house in houses:
        # make a list for storing the distances of the house to each battery
        distances: list[int] = []

        # get the distance to each battery
        for battery in batteries:
            distances.append(house.distance_to_any_battery(battery))

        # get the closest battery
        closest_battery_idx = distances.index(min(distances))
        closest_battery = batteries[closest_battery_idx]

        # connect the house to the closest battery without loading it
        closest_battery.connect_home_without_load(house)


def move_batteries_to_center(grid: Grid) -> None:
    """
    Moves all batteries on the grid to the center of its connected houses.

    Pre : grid is a Grid object with connected houses
    Post: the batteries are moved to the center of its connected houses, if
          a house is on this center, it is randomly moved to on of the
          neighbouring cells
    """

    for battery in grid.batteries:
        # find rounded coordinates of the center of its connected houses
        new_x, new_y = get_new_center_battery(battery)

        # check if new location is not the same as it already is
        if (new_x, new_y) != (battery.coord_x, battery.coord_y):
            # move to this coordinate if free, if not check for a free spot
            # around it
            while not grid.move_battery(battery, new_x, new_y):
                # move randomly
                offset_x, offset_y = get_random_offset()
                new_x += offset_x
                new_y += offset_y


def get_new_center_battery(battery: Battery) -> tuple[int, int]:
    """
    Gets the center of the connected houses of the battery.

    Pre : battery is a Battery object
    Post: a tuple of two integers is returned in the format (new_x, new_y), if
          no houses are connected, the original coordinates are returned
    """

    # get the connected houses to the battery
    connected_houses = battery.connected_homes

    # check if there are actually houses connected
    if len(connected_houses) != 0:
        # set variables for calculating the center
        total_x, total_y = 0, 0
        n_houses = len(connected_houses)

        # go over all connected houses and add up the x and y coordinates
        for house in connected_houses:
            total_x += house.coord_x
            total_y += house.coord_y

        # get the average coordinates
        center_x = int(round(total_x/n_houses))
        center_y = int(round(total_y/n_houses))

        return (center_x, center_y)

    # return original coordinates
    return (battery.coord_x, battery.coord_y)


def get_random_offset() -> tuple[int, int]:
    """
    Get a random offset for a coordinate.

    Post: a tuple of two integers is returned where each integer is a random
          choice in [-1, 0, 1]
    """

    offsets = [-1, 0, 1]

    return (choice(offsets), choice(offsets))
