import numpy as np
from random import randint
from random import choice

from ...classes.grid import Grid
from ...classes.house import House
from ...classes.battery import Battery
from code.visualization.visualization import visualize
from ..own_cables.greedy import greedy
from ..shared_cables.hill_climber_shared import init_hill_climber_shared


def clustering(grid: Grid) -> Grid:
    """"
    Clusters the batteries on a grid according to the houses using K-means
        clustering.
    
    Pre : grid is a Grid object with no connections and no cables
    Post: the batteries are clustered and connections are made using the greedy
        algorithm, the grid is then returned
    """
    # * ALGORITHM PARAMETERS
    n_iterations = 10
    visualize_clustering = False

    # randomly place batteries
    random_place_batteries(grid)

    # visualisatie
    if visualize_clustering:
        grid.cost = 99999999999
        print("random battery placement without connections")
        visualize(grid)

    for _ in range(n_iterations):
        # go over all houses and find their manhattan distances to the
        # batteries connect the closest houses first and stop when a battery
        # is maxed
        connect_closest_houses(grid)

        # visualisatie
        if visualize_clustering:
            print(f"{_}: batteries connected but not moved")
            grid.lay_shared_cables()
            visualize(grid)

        # find the center of the connected houses
        move_batteries_to_center(grid)

        # visualisatie
        if visualize_clustering:
            grid.remove_cables()

        # remove all connections
        grid.remove_all_connections()

    # perform the connection algorithm
    print("Perform greedy")
    grid = greedy(grid)

    # lay the cables
    grid.lay_shared_cables()

    # ! TESTEN
    # grid = init_hill_climber_shared(grid)
    

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
    # ! DIT KAN VEEL KORTER
    # connect gelijk het dichtsbijzijnde huis


    all_houses_distances: list[tuple[House, list[int]]] = []

    # loop over all houses
    for house in grid.houses:
        house_distances: list[int] = []

        # find distances to every battery
        for battery in grid.batteries:
            house_distances.append(house.distance_to_any_battery(battery))

        all_houses_distances.append((house, house_distances))

    # sort all houses on their minimum distance to a battery
    all_houses_distances.sort(key=lambda x: min(x[1]))

    # go over all houses and connect to closest battery if possible
    for house_and_distances in all_houses_distances:
        house, distances = house_and_distances

        # find minimum distance
        min_distance = min(distances)

        # find the battery with this minimum distance
        closest_battery_index = distances.index(min_distance)
        closest_battery = grid.batteries[closest_battery_index]

        # connect without loading the battery
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

    Post: a tuple of two integers where each integer is a random choice in
        [-1, 0, 1]
    """
    offsets = [-1, 0, 1]
    return (choice(offsets), choice(offsets))

