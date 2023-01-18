from ...classes.grid import Grid
from ...classes.house import House
from ...classes.battery import Battery
from ...helper_functions.valid_solution import valid_solution
from ...helper_functions.resolve_error import resolve_error


def greedy(grid: Grid) -> Grid:
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

    grid.calc_cost_normal()

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
