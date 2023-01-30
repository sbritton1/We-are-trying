from copy import deepcopy
from math import ceil
from random import shuffle
import multiprocessing
import matplotlib.pyplot as plt

from ...classes.grid import Grid
from ...helper_functions.valid_solution import valid_solution
from ...helper_functions.resolve_error import resolve_error
from ...helper_functions.add_random_connections import add_random_connections
from ...helper_functions.find_random_houses import find_random_houses
from ...helper_functions.swap_houses import swap_houses
from ..own_cables.greedy import greedy


def plant_propagation(grid: Grid) -> Grid:

    # * set algorithm parameters
    shared_cables = True
    n_roots = 8
    min_runners = 2
    max_runners = 5
    min_changes = 10
    max_changes = 50
    n_generations = 20
    print_stuff = True
    plot_stuff = True

    # get the starting point for the plant propagation algorithm
    root_grids = get_start_roots(grid, n_roots)

    # store the best cost of each generation
    best_costs: list[int] = []

    # go over the generations
    for _ in range(n_generations):
        # print the generation number
        if print_stuff:
            print(_)

        # get the runners of the new generation
        runners = create_new_generation(root_grids, min_runners,
                                        max_runners, min_changes,
                                        max_changes, shared_cables,
                                        print_stuff)

        # sort runners in ascending order of cost
        runners.sort(key=lambda x: x.calc_cost_shared())

        # set the best runners as the new roots
        root_grids = runners[:n_roots]

        # store the best score
        best_costs.append(root_grids[0].calc_cost_shared())

    if plot_stuff:
        plot_results(best_costs, grid, n_generations)

    # choose the best runner of the last generation
    best_runner = runners[0]

    # remove the cables of the best runner
    best_runner.remove_cables()

    return best_runner


def get_start_roots(grid: Grid, n_roots: int) -> list[Grid]:
    # make a list to store the temporary grids
    start_roots: list[Grid] = []

    # repeat n_roots times
    for _ in range(n_roots * 5):
        # make a copy of the grid
        tmp_grid: Grid = deepcopy(grid)

        # # make random connections
        # tmp_grid = add_random_connections(tmp_grid)

        # # resolve errors untill grid is valid
        # while valid_solution(tmp_grid) is False:
        #     resolve_error(tmp_grid)

        tmp_grid = greedy(tmp_grid)

        # lay the shared cables
        tmp_grid.lay_shared_cables()


        start_roots.append(tmp_grid)

    # sort runners in ascending order of cost
    start_roots.sort(key=lambda x: x.calc_cost_shared())

    # return the best n_roots roots
    return start_roots[:n_roots]


def create_new_generation(root_grids: list[Grid], min_runners: int,
                          max_runners: int, min_changes: int, max_changes: int,
                          shared_cables: bool, print_stuff: bool
                          ) -> list[Grid]:

    # variables for keeping track of the costs (set to arbitrary values)
    lowest_cost: int = 9999999
    highest_cost: int = 0

    # go over each grid and check for the highest and lowest cost
    for root_grid in root_grids:
        cost = calculate_cost(root_grid, shared_cables)
        if cost < lowest_cost:
            lowest_cost = cost
        if cost > highest_cost:
            highest_cost = cost

    # create a work list for the multithreading
    work = []

    # go over all the roots to make the runners
    for root_grid in root_grids:
        # determine the fitness of the root
        fitness = get_fitness(root_grid.cost, lowest_cost, highest_cost)

        # based on the fitness, decide the amount of runners and their distance
        n_runners = get_n_runners(fitness, max_runners, min_runners)
        n_changes = get_n_changes(fitness, max_changes, min_changes)

        if print_stuff:
            print(f"Grid cost: {root_grid.cost}, fitness: {fitness}, n_runners: {n_runners}, n_changes: {n_changes}")

        # create each runner
        for _ in range(n_runners):
            # make a copy of the root
            runner = deepcopy(root_grid)

            # append the work for the multiprocessing to the work list
            work.append((runner, n_changes))

    # the amount of threads that will be used
    workers = 8

    # multiprocessing stuff
    p = multiprocessing.Pool(workers)

    # run the process to get the runners list
    runners: list[Grid] = p.starmap(make_change, work)

    return root_grids + runners


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


def make_change(grid: Grid, n_changes: int) -> Grid:
    # make a change n_changes times
    for _ in range(n_changes):
        # shuffle the houses list of the grid
        # shuffle(grid.houses)

        # find random houses in the grid
        house1, house2 = find_random_houses(grid)

        # perform swap
        swap_houses(house1, house2)

        # remove and then lay the cables back
        grid.remove_cables()
        grid.lay_shared_cables()

    return grid


def plot_results(best_costs: list[int], grid: Grid, n_generations: int) -> None:
    plt.title(f"Plot of best costs per generation (algorithm: plant propagation, district: " + \
              f"{grid.district}, generations: {n_generations})")
    plt.plot(best_costs)
    plt.xlabel("Generation")
    plt.ylabel("Best cost")
