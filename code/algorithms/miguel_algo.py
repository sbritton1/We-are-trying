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

    improve_solution(grid)

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

    battery_weights = []
    for battery in grid.batteries:
        battery_weights.append(battery.current_capacity)

    best_bat = random.choices(grid.batteries, weights=battery_weights, k=1)[0]

    if best_bat.is_connection_possible(unconnected) is True:
        best_bat.connect_home(unconnected)
        unconnected.make_connection(best_bat)
        return

    for i in range(10000):
        house_weights = []
        for house in best_bat.connected_homes:
            house_weights.append(1/house.maxoutput)

        house = random.choices(best_bat.connected_homes, weights=house_weights, k=1)[0]

        if house.maxoutput + best_bat.current_capacity > unconnected.maxoutput:
            best_bat.disconnect_home(house)
            house.delete_connection()

            best_bat.connect_home(unconnected)
            unconnected.make_connection(best_bat)

            resolve_error(grid)

            return


def improve_solution(grid: Grid) -> None:
    improve_loc = 0

    while True:
        grid.houses.sort(key=lambda house: house.distance_to_battery(), reverse=True)

        best_improvement: int = 0
        target: House = None

        for house in grid.houses[improve_loc:]:
            if possible_swap(grid.houses[improve_loc], house) is True:
                improvement = calc_improvement(grid.houses[improve_loc], house)
                if improvement > best_improvement:
                    best_improvement = improvement
                    target = house

        if best_improvement == 0:
            improve_loc += 1
            if improve_loc == len(grid.houses):
                return

        else:
            swap_houses(grid.houses[improve_loc], target)


def possible_swap(house1: House, house2: House) -> bool:
    if house1.maxoutput > house2.maxoutput + house2.connection.current_capacity:
        return False

    elif house2.maxoutput > house1.maxoutput + house1.connection.current_capacity:
        return False

    return True


def calc_improvement(house1: House, house2: House) -> int:
    diff1 = house1.distance_to_battery() - house1.distance_to_any_battery(house2.connection)
    diff2 = house2.distance_to_battery() - house2.distance_to_any_battery(house1.connection)

    return diff1 + diff2


def swap_houses(house1: House, house2: House):
    house1_bat: Battery = house1.connection
    house2_bat: Battery = house2.connection

    house1_bat.disconnect_home(house1)
    house1.delete_connection()
    house2_bat.disconnect_home(house2)
    house2.delete_connection()

    house1_bat.connect_home(house2)
    house2.make_connection(house1_bat)
    house2_bat.connect_home(house1)
    house1.make_connection(house2_bat)
