from ...classes.grid import Grid
from ...classes.house import House
from ...helper_functions.valid_solution import valid_solution
from ...helper_functions.resolve_error import resolve_error
from ...helper_functions.add_random_connections import add_random_connections
from ...helper_functions.swap_houses import swap_houses
from ...helper_functions.possible_swap import possible_swap
from ...helper_functions.find_random_houses import find_random_houses
from ..own_cables.greedy import greedy
import copy
import multiprocessing

def init_hill_climber_battery(grid: Grid):
    # create list of grids as work for multithreading
    grids: list[Grid] = []

    # amount of grids to run algorithm on
    for i in range(1):

        # create deepcopy to not mess with original
        tmp_grid = copy.deepcopy(grid)
        tmp_grid = greedy(tmp_grid)

        tmp_grid.lay_shared_cables()
        tmp_grid.calc_cost_shared()

        grids.append(tmp_grid)

    # use multithread processing, with workers amount of threads
    workers = 1
    p = multiprocessing.Pool(workers)
    results = (p.map(work, grids))

    # keeps track of costs of all solutions
    costs_best_solution: list[int] = []
    lowest_cost: int = None
    best_solution: Grid = None

    # loop through results to find best one
    for result in results:
        tmp_grid: Grid = result[0]
        costs: list[int] = result[1]
        if lowest_cost is None or tmp_grid.cost < lowest_cost:
            costs_best_solution = costs
            lowest_cost = tmp_grid.cost
            best_solution = tmp_grid

    best_solution.remove_cables()
    return best_solution

def work(grid):
    pass