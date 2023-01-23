from copy import deepcopy
from math import ceil
from random import shuffle
import multiprocessing

from ...classes.grid import Grid
from ...classes.battery import Battery
from ...classes.house import House
from ...helper_functions.valid_solution import valid_solution
from ...helper_functions.resolve_error import resolve_error
from ...helper_functions.add_random_connections import add_random_connections
from ...helper_functions.find_random_houses import find_random_houses
from ...helper_functions.possible_swap import possible_swap
from ...helper_functions.swap_houses import swap_houses
from .sd_hill_climber_shared import sd_hill_climber_shared
from .hill_climber_shared import hill_climber_shared

def plant_propagation(grid: Grid) -> Grid:
    
    # * set algorithm parameters
    shared_cables = True
    min_runners = 1
    max_runners = 7
    min_changes = 2
    max_changes = 40
    n_generations = 20

    # get the starting point for the plant propagation algorithm
    root_grids = get_start_roots(grid, max_runners)

    # go over the generations
    for _ in range(n_generations):
        print(_)
        runners = create_new_generation(root_grids, min_runners,
                                           max_runners, min_changes,
                                           max_changes, shared_cables)
        
        # sort runners in ascending order of cost
        runners.sort(key=lambda x: x.calc_cost_shared())
        
        # set the best runners as the new roots
        root_grids = runners[:max_runners]    

    # choose the best runner of the last generation
    best_runner = runners[0]

    # remove the cables of the best runner
    best_runner.remove_cables()
    
    return best_runner 


def get_start_roots(grid: Grid, n_roots: int) -> list[Grid]:
    # make a list to store the temporary grids
    start_roots: list[Grid] = []
    
    for _ in range(n_roots):
        tmp_grid: Grid = deepcopy(grid)
        tmp_grid = add_random_connections(tmp_grid)

        while valid_solution(tmp_grid) is False:
            resolve_error(tmp_grid)

        tmp_grid.lay_shared_cables()

        start_roots.append(tmp_grid)
    
    return start_roots


def create_new_generation(root_grids: list[Grid], min_runners: int,
                          max_runners: int, min_changes: int, max_changes: int,
                          shared_cables: bool):

    # keeps track of costs of all solutions
    lowest_cost: int = None
    highest_cost: int = None

    # go over each grid and check for the highest and lowest cost
    for root_grid in root_grids:
        cost = calculate_cost(root_grid, shared_cables)
        if lowest_cost is None or cost < lowest_cost:
            lowest_cost = cost
        if highest_cost is None or cost > highest_cost:
            highest_cost = cost

    # determine the fitness and thus how many runners should be created and how
    # far each runner should go

    work = []

    for root_grid in root_grids:
        fitness = get_fitness(root_grid.cost, lowest_cost, highest_cost)

        n_runners = get_n_runners(fitness, max_runners, min_runners)

        n_changes = get_n_changes(fitness, max_changes, min_changes)

        print(f"Grid cost: {root_grid.cost}, fitness: {fitness}, n_runners: {n_runners}, n_changes: {n_changes}")

        for _ in range(n_runners):
            runner = deepcopy(root_grid)
            work.append((runner, n_changes))

    workers = 4
    p = multiprocessing.Pool(workers)
    runners: list[Grid] = p.starmap(make_change, work)

    return runners


def calculate_cost(grid: Grid, shared_cables: bool) -> int:
    if shared_cables:
        return grid.calc_cost_shared()
    return grid.calc_cost_normal()


def get_fitness(cost: int, lowest_cost: int, highest_cost: int) -> float:
    return (highest_cost - cost) / (highest_cost - lowest_cost)


def get_n_changes(fitness: float, max_changes: int, min_changes: int) -> int:
    return ceil((1 - fitness) * (max_changes - min_changes)) + min_changes


def get_n_runners(fitness: float, max_runners: int, min_runners: int) -> int:
    return ceil(fitness * (max_runners - min_runners)) + min_runners


def make_change(grid: Grid, n_changes) -> Grid:
    for _ in range(n_changes):
        shuffle(grid.houses)

        house1, house2 = find_random_houses(grid)
                        
        # perform swap
        swap_houses(house1, house2)

        # remove and then lay the cables back
        grid.remove_cables()
        grid.lay_shared_cables()

    return grid   
  