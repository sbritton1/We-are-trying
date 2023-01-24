from random import randint

from ...classes.grid import Grid
from ...classes.house import House
from ...classes.battery import Battery


def clustering(grid: Grid) -> Grid:


    # randomly place batteries
    random_place_batteries(grid)

    # go over all houses and find their manhattan distances to the batteries
    # connect the closest houses first and stop when a battery is maxed
    connect_closest_houses(grid)

    # find the center of the connected houses

    # repeat set times


def random_place_batteries(grid: Grid) -> None:
    max_x, max_y = grid.max_x, grid.max_y

    for battery in grid.batteries:
        random_x, random_y = get_random_coordinates(max_x, max_y)

        while grid.move_battery(battery, random_x, random_y) is False:
            random_x, random_y = get_random_coordinates(max_x, max_y)


def get_random_coordinates(max_x: int, max_y: int) -> tuple[int, int]:
    return (randint(0, max_x), randint(0, max_y))


def connect_closest_houses(grid: Grid) -> Grid:
    all_houses_distances: list[list[int]] = []

    # loop over all houses
    for house in grid.houses:
        house_distances: list[int] = []

        # find distances to every battery
        for battery in grid.batteries:
            house_distances.append(house.distance_to_any_battery(battery))

        all_houses_distances.append(house_distances)
    
    all_houses_distances.sort(key=lambda x: min(x))


