from ...classes.grid import Grid
from ...classes.battery import Battery
from ...helper_functions.valid_solution import valid_solution
from ...helper_functions.resolve_error import resolve_error


def greedy(grid: Grid) -> Grid:
    """
    Uses a greedy algorithm to find a solution for the case,
    wherein cables are not shared.

    pre : grid is of class Grid
    post: returns a grid of class Grid wherein each house
          is connected to a battery
    """

    # keep track of which houses aren't connected yet
    unconnected: list[int] = [*range(len(grid.houses))]

    for i in range(len(grid.houses)):

        # call function to find unconnected house closes to available battery
        minimum = find_minimum(grid, unconnected)
        if minimum == (None, None):
            break

        battery = minimum[0]
        house = grid.houses[minimum[1]]

        # connect house from battery and remove it from unconnected
        house.make_connection(battery)
        battery.connect_home(house)
        unconnected.remove(minimum[1])

    # makes sure solution is valid
    while valid_solution(grid) is False:
        resolve_error(grid)

    # calculate cost of solution
    grid.calc_cost_normal()

    return grid


def find_minimum(grid: Grid, unconnected: list[int]) -> tuple[Battery, int]:
    """
    Finds unconnected house that is closest to a battery with enough capacity
    to be able to make a connection.

    pre : grid is of class Grid, unconnected is list of ints
    post: returns tuple of class Battery and an integer, wherein the
          integer the index is of the house in grid.houses that has
          to be connected to the battery
    """

    min_distance = 1000
    minimum = (None, None)

    # loop through each battery and unconnected house
    for battery in grid.batteries:
        for i in unconnected:
            distance = grid.houses[i].distance_to_any_battery(battery)
            possible_connection = battery.is_connection_possible(grid.houses[i])

            # store battery and house index if it's current best option
            if distance < min_distance and possible_connection:
                min_distance = distance
                minimum = (battery, i)

    return minimum
