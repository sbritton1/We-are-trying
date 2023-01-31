from ...classes.grid import Grid
from ...classes.battery import Battery
from ...classes.house import House
from ...helper_functions.valid_solution import valid_solution
from ...helper_functions.resolve_error import resolve_error
from typing import Any
import copy


def greedy(grid: Grid) -> Grid:
    """
    Uses a greedy algorithm to find a solution for the case,
    wherein cables are not shared.

    Pre : grid is of class Grid
    Post: returns a grid of class Grid wherein each house
          is connected to a battery
    """

    # make a list to keep track of which houses aren't connected yet
    unconnected: list[int] = [*range(len(grid.houses))]

    for _ in range(len(grid.houses)):

        # call function to find unconnected house closes to available battery
        minimum: tuple[Any, Any] = find_minimum(grid, unconnected)

        # if there was no battery available, break
        if minimum == (None, None):
            break

        # get the house and battery objects that should be connected
        battery: Battery = minimum[0]
        house: House = grid.houses[minimum[1]]

        # connect house to battery
        house.make_connection(battery)
        battery.connect_home(house)

        # remove the house-index from the unconnected list
        unconnected.remove(minimum[1])

    # check if the solution is valid and if not fix it
    if valid_solution(grid) is False:
        grid = find_best_resolve_error(grid)

    return grid


def find_minimum(grid: Grid, unconnected: list[int]) -> tuple[Any, Any]:
    """
    Finds unconnected house that is closest to a battery with enough capacity
    to be able to make a connection.

    Pre : grid is of class Grid, unconnected is a list of integers
    Post: returns tuple of class Battery and an integer, where the
          integer is the index of the house in grid.houses that has
          to be connected to the battery
    """

    # choose an arbitrarily high number for the minimal distance
    min_distance: int = 1000

    minimum: tuple[Any, Any] = (None, None)

    # loop through each battery and unconnected house
    for battery in grid.batteries:
        for i in unconnected:
            distance: int = grid.houses[i].distance_to_any_battery(battery)
            possible_connection: bool = battery.is_connection_possible(grid.houses[i])

            # store battery and house index if it's current best option
            if distance < min_distance and possible_connection:
                min_distance = distance
                minimum = (battery, i)

    return minimum


def find_best_resolve_error(grid: Grid) -> Grid:
    """
    If an error needs to be resolved, this function will try to
    resolve it multiple times and will return the best found solution.

    Pre : grid is of class Grid
    Post: returns Grid of valid solution
    """

    # choose an arbitrarily high value for the best cost
    best_cost: int = 100000

    best_solution: Grid = None

    # set the amount of times it tries to find for an improvement
    n_tries = 1000

    for _ in range(n_tries):
        tmp_grid = copy.deepcopy(grid)

        resolve_try = 0

        # occasionally a valid solution won't be found, so try max 10 times
        while valid_solution(tmp_grid) is False and resolve_try < 10:
            resolve_error(tmp_grid)
            resolve_try += 1

        # store result if it is an improvement
        cost = tmp_grid.calc_cost_normal()
        if valid_solution(tmp_grid) and cost < best_cost:
            best_cost = cost
            best_solution = tmp_grid

    return best_solution
