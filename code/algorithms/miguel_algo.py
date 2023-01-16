from ..classes.grid import Grid
from ..classes.house import House
from ..classes.battery import Battery
from .valid_solution import valid_solution
import random

def miguel_algo(grid: Grid) -> Grid:
    unconnected: list[int] = [*range(len(grid.houses))]

    for i in range(len(grid.houses)):
        minimum = find_minimum(grid, unconnected)
        if minimum == (None, None):
            break

        battery = minimum[0]
        house = grid.houses[minimum[1]]
        unconnected.remove(minimum[1])

        house.make_connection(battery)
        battery.connect_home(house)

    while valid_solution(grid) is False:
        resolve_error(grid)

    grid.calc_cost()
    
    return grid


def find_minimum(grid: Grid, unconnected: list[int]) -> tuple[Battery, int]:
    min_distance = 100
    minimum = (None, None)

    for battery in grid.batteries:
        for i in unconnected:
            distance = grid.houses[i].distance_to_any_battery(battery)
            possible_connection = battery.is_connection_possible(grid.houses[i])
            if distance < min_distance and possible_connection:
                min_distance = distance
                minimum = (battery, i)

    return minimum


def resolve_error(grid: Grid) -> None:
    unconnected: House = None

    for house in grid.houses:
        if house.has_connection is False:
            unconnected = house

    # grid.batteries.sort(key=lambda battery: battery.current_capacity, reverse=True)

    battery_weights = []
    for battery in grid.batteries:
        battery_weights.append(battery.current_capacity)

    best_bat = random.choices(grid.batteries, weights=battery_weights, k=1)[0]


    #######################################
    print("\n")
    print(unconnected.maxoutput)
    for battery in grid.batteries:
        print(battery.current_capacity)
    print("\n")
    #######################################

    if best_bat.is_connection_possible(unconnected) is True:
        print("check")
        best_bat.connect_home(unconnected)
        unconnected.make_connection(best_bat)
        return

    # best_bat.connected_homes.sort(key=lambda house: house.maxoutput, reverse=False)

    while True:
        house_weights = []
        for house in best_bat.connected_homes:
            house_weights.append(1/house.maxoutput)

        house = random.choices(best_bat.connected_homes, weights=house_weights, k=1)[0]
        print(house.maxoutput, best_bat.current_capacity, unconnected.maxoutput)
        if house.maxoutput + best_bat.current_capacity > unconnected.maxoutput:
            best_bat.disconnect_home(house)
            house.delete_connection()

            best_bat.connect_home(unconnected)
            unconnected.make_connection(best_bat)

            resolve_error(grid)

            return




