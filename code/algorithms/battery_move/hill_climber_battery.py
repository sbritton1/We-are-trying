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

    return

def work(grid: Grid):
    """
    Runs the simulated annealing and returns the
    grid and costs.

    Pre:  grid of class grid
    Post: tuple containing grid of class grid and integer
    """

    # run algorithm and return the result
    run_algo = hill_climber_battery(grid)
    grid: Grid = run_algo[0]
    costs = run_algo[1]
    print(grid.cost)
    return (grid, costs)

def hill_climber_battery(grid: Grid):
    org_cost: int = grid.cost
    last_improvement = 0
    iteration = 0

    while last_improvement < 0 and iteration < 1000:
        tmp_grid: Grid = copy.deepcopy(grid)
        tmp_grid.remove_cables()
        tmp_grid.remove_connections()
        
        tmp_grid = move_battery(tmp_grid)
        tmp_grid = greedy(tmp_grid)
        tmp_grid.lay_shared_cables()
        new_cost = tmp_grid.calc_cost_shared()

        if new_cost < org_cost:
            grid = tmp_grid
            org_cost = new_cost
            last_improvement = iteration
        
        iteration += 1

def move_battery():
    pass