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

    n_iterations = 10
    visualize_clustering = False

    # randomly place batteries
    random_place_batteries(grid)

    grid.cost = 99999999999

    if visualize_clustering:
        print("random battery placement without connections")
        visualize(grid)

    for _ in range(n_iterations):
        # go over all houses and find their manhattan distances to the batteries
        # connect the closest houses first and stop when a battery is maxed
        connect_closest_houses(grid)

        if visualize_clustering:
        # ! VISUALISATIE
            print(f"{_}: batteries connected but not moved")
            grid.lay_shared_cables()
            visualize(grid)

        # find the center of the connected houses
        move_batteries_to_center(grid)

        if visualize_clustering:
            # ! VISUALISATIE
            grid.remove_cables()

        # remove all connections
        grid.remove_all_connections()

    print("Perform greedy")
    grid = greedy(grid)
    grid.lay_shared_cables()
    print(f"Cost after greedy is {grid.calc_cost_shared()}")
    grid.remove_cables()


    # grid = init_hill_climber_shared(grid)
    

    return grid


def random_place_batteries(grid: Grid) -> None:
    max_x, max_y = grid.max_x, grid.max_y

    for battery in grid.batteries:
        random_x, random_y = get_random_coordinates(max_x, max_y)

        while grid.move_battery(battery, random_x, random_y) is False:
            random_x, random_y = get_random_coordinates(max_x, max_y)


def get_random_coordinates(max_x: int, max_y: int) -> tuple[int, int]:
    return (randint(0, max_x), randint(0, max_y))


def connect_closest_houses(grid: Grid) -> None:
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

