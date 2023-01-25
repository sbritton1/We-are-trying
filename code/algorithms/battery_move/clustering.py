import numpy as np
from random import randint
from random import choice

from ...classes.grid import Grid
from ...classes.house import House
from ...classes.battery import Battery
from code.visualization.visualization import visualize



def clustering(grid: Grid) -> Grid:

    n_iterations = 5

    # randomly place batteries
    random_place_batteries(grid)

    for _ in range(n_iterations):
        # go over all houses and find their manhattan distances to the batteries
        # connect the closest houses first and stop when a battery is maxed
        connect_closest_houses(grid)

        # find the center of the connected houses
        move_batteries_to_center(grid)

        # remove all connections
        grid.remove_all_connections()

    print(f"{grid.batteries[0].coord_x}, {grid.batteries[0].coord_y}")

    grid.cost = 99999999999
    visualize(grid)


def random_place_batteries(grid: Grid) -> None:
    max_x, max_y = grid.max_x, grid.max_y

    for battery in grid.batteries:
        random_x, random_y = get_random_coordinates(max_x, max_y)

        while grid.move_battery(battery, random_x, random_y) is False:
            random_x, random_y = get_random_coordinates(max_x, max_y)


def get_random_coordinates(max_x: int, max_y: int) -> tuple[int, int]:
    return (randint(0, max_x), randint(0, max_y))


def connect_closest_houses(grid: Grid) -> None:
    all_houses_distances: list[list[int]] = []

    # loop over all houses
    for house in grid.houses:
        house_distances: list[int] = []

        # find distances to every battery
        for battery in grid.batteries:
            house_distances.append(house.distance_to_any_battery(battery))

        all_houses_distances.append(house_distances)
    
    # sort all houses on their minimum distance to a battery
    all_houses_distances.sort(key=lambda x: min(x))

    # go over all houses and connect to closest battery if possible
    for i, house in enumerate(grid.houses):
        # find minimum distance
        house_distances = all_houses_distances[i]
        min_distance = min(house_distances)
        
        # find the battery with this minimum distance
        closest_battery_index = house_distances.index(min_distance)
        closest_battery = grid.batteries[closest_battery_index]

        # connect without loading the battery
        closest_battery.connect_home_without_load(house)
        


def move_batteries_to_center(grid: Grid) -> None:
    for battery in grid.batteries:
        # find rounded coordinates of the center of its connected houses
        new_x, new_y = get_new_center_battery(battery)

        # check if new location is not the same as it already is
        if (new_x, new_y) != (battery.coord_x, battery.coord_y):
            # move to this coordinate if free, if not check for a free spot around it
            while not grid.move_battery(battery, new_x, new_y):
                # move randomly
                offset_x, offset_y = get_random_offset()
                new_x += offset_x
                new_y += offset_y


def get_new_center_battery(battery: Battery) -> tuple[int, int]: 
    connected_houses = battery.connected_homes
    if len(connected_houses) != 0:    
        total_x, total_y = 0, 0
        n_houses = len(connected_houses)

        for house in connected_houses:
            total_x += house.coord_x
            total_y += house.coord_y

        center_x = int(round(total_x/n_houses))
        center_y = int(round(total_y/n_houses))

        return (center_x, center_y)
    return (battery.coord_x, battery.coord_y)

def get_random_offset() -> tuple[int, int]:
    offsets = [-1, 0, 1]
    return (choice(offsets), choice(offsets))

