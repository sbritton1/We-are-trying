from ...classes.grid import Grid
from ...classes.house import House
from ...helper_functions.valid_solution import valid_solution
from ...helper_functions.resolve_error import resolve_error
from ...helper_functions.add_random_connections import add_random_connections
from ...helper_functions.possible_swap import possible_swap
from ...helper_functions.swap_houses import swap_houses
import copy


def init_sd_hill_climber(grid: Grid) -> Grid:
    """
    Initializes grids for the steepest descent hill climber
    algorithm to improve, optimized for non-shared cables.

    Pre : grid is of class Grid
    Post: returns best found solution for grid
    """

    # keeps track of costs of all solutions
    lowest_cost: int = None
    best_solution: Grid = None

    # number of times to run the algorithm
    for i in range(100):
        tmp_grid: Grid = copy.deepcopy(grid)
        tmp_grid = add_random_connections(tmp_grid)

        # if not every house is connected, resolve for valid solution
        while valid_solution(tmp_grid) is False:
            resolve_error(tmp_grid)

        # run steepest decline hill climber
        sd_hill_climber(tmp_grid)

        cost: int = tmp_grid.calc_cost_normal()

        # check if found solution is best solution
        if lowest_cost is None or cost < lowest_cost:
            lowest_cost = cost
            best_solution = tmp_grid

        print(i)

    return best_solution


def sd_hill_climber(grid: Grid) -> None:
    """
    Steepest descent hill climber algorithm.

    Pre : grid is of class Grid
    Post: algorithm has swapped houses until local
          minimum has been reached.
    """

    while True:

        # keep track of best possible swap
        best_improvement: int = 0
        target1: House = None
        target2: House = None

        # loop through possible swap of houses
        for house1 in grid.houses:
            for house2 in grid.houses:
                if house1.connection != house2.connection:

                    # Check improvement if swap is possible
                    if possible_swap(house1, house2) is True:
                        improvement = calc_improvement(house1, house2)
                        if improvement > best_improvement:
                            best_improvement = improvement
                            target1 = house1
                            target2 = house2

        # return when no more improvements can be found
        if best_improvement == 0:
            return

        else:
            swap_houses(target1, target2)


def calc_improvement(house1: House, house2: House) -> int:
    """
    Calculates the improvement of a swap of the houses based
    on the manhattan distance difference.

    Pre : house1 and house2 are of class House
    Post: returns int value of improvement. improvement is
          negative when the swap increases the cost of the grid
    """

    diff1 = house1.distance_to_battery() - house1.distance_to_any_battery(house2.connection)
    diff2 = house2.distance_to_battery() - house2.distance_to_any_battery(house1.connection)

    return diff1 + diff2
