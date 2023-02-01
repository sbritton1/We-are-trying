from copy import deepcopy
from math import ceil
import multiprocessing
import matplotlib.pyplot as plt

from ...classes.grid import Grid
from ...helper_functions.valid_solution import valid_solution
from ...helper_functions.resolve_error import resolve_error
from ...helper_functions.add_random_connections import add_random_connections
from ...helper_functions.find_random_houses import find_random_houses
from ...helper_functions.swap_houses import swap_houses


def plant_propagation(grid: Grid) -> Grid:
    """
    Find an optimal solution for the Smart Grid problem with shared cables
    using the Plant Propagation Algorithm.

    Pre : grid is a Grid object with no connections between houses and
          batteries and no cables
    Post: the best found grid is returned with connections but no cables
    """

    # * set algorithm parameters
    n_roots = 8
    min_runners = 2
    max_runners = 6
    min_changes = 1
    max_changes = 8
    n_generations = 300
    max_times_no_improvement = 20

    # * set the feedback methods
    print_stuff = True
    plot_stuff = True

    # get the starting point for the plant propagation algorithm
    root_grids = get_start_roots(grid, n_roots)

    # store the best cost of each generation
    best_costs: list[int] = []

    # set variables for stopping when no improvements are detected
    current_generation = 0
    n_times_no_improvement = 0

    # go over the generations
    for _ in range(n_generations):
        # print the generation number
        if print_stuff:
            print(_)

        # get the runners of the new generation
        runners = create_new_generation(root_grids, min_runners,
                                        max_runners, min_changes,
                                        max_changes, print_stuff)

        current_generation += 1

        # sort runners in ascending order of cost
        runners.sort(key=lambda x: x.calc_cost_shared())

        # set the best runners as the new roots
        root_grids = runners[:n_roots]

        # get the best score
        best_cost = root_grids[0].calc_cost_shared()

        # check if there was an improvement
        if best_costs and best_cost == best_costs[-1]:
            n_times_no_improvement += 1
            if n_times_no_improvement == max_times_no_improvement:
                print(f"Stopped after {current_generation} generations")

                break
        else:
            n_times_no_improvement = 0

        best_costs.append(best_cost)

    # plot the best results of each generation, if plot_stuff is set to True
    if plot_stuff:
        plot_results(best_costs, grid, current_generation)

    # choose the best runner of the last generation
    best_runner = runners[0]

    # remove the cables of the best runner
    best_runner.remove_cables()

    return best_runner


def get_start_roots(grid: Grid, n_roots: int) -> list[Grid]:
    """
    Creates random start roots for the PPA.

    Pre : grid is a Grid object with no connections and cables and n_roots is
          an integer
    Post: a list of n_roots Grid objects is returned with random connections
          that still give a valid solution
    """

    # make a list to store the temporary grids
    start_roots: list[Grid] = []

    # get n_roots * 3 random start roots and pick the best
    for _ in range(n_roots * 3):
        # make a copy of the grid
        tmp_grid: Grid = deepcopy(grid)

        # make random connections
        tmp_grid = add_random_connections(tmp_grid)

        # resolve errors untill grid is valid
        while valid_solution(tmp_grid) is False:
            resolve_error(tmp_grid)

        # lay the shared cables
        tmp_grid.lay_shared_cables()

        start_roots.append(tmp_grid)

    # sort runners in ascending order of cost
    start_roots.sort(key=lambda x: x.calc_cost_shared())

    # return the best n_roots roots
    return start_roots[:n_roots]


def create_new_generation(root_grids: list[Grid], min_runners: int,
                          max_runners: int, min_changes: int, max_changes: int,
                          print_stuff: bool) -> list[Grid]:
    """
    Creates a new generation of grids according to the PPA.

    Pre : the set type hints match, all root grids have no connections and
          cables, min_runners < max_runners, min_changes < max)changes
    Post: a list of grids is returned, containing all the original root grids
          and their runners
    """

    # variables for keeping track of the costs (set to arbitrary values)
    lowest_cost: int = 9999999
    highest_cost: int = 0

    # go over each grid and check for the highest and lowest cost
    for root_grid in root_grids:
        cost = root_grid.calc_cost_shared()
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
            print(
                f"Grid cost: {root_grid.cost}, fitness: {fitness}," +
                f"n_runners: {n_runners}, n_changes: {n_changes}"
                )

        # create each runner
        for _ in range(n_runners):
            # make a copy of the root
            runner = deepcopy(root_grid)

            # append the work for the multiprocessing to the work list
            work.append((runner, n_changes))

    # the amount of threads that will be used
    workers = 4

    # multiprocessing stuff
    p = multiprocessing.Pool(workers)

    # run the process to get the runners list
    runners: list[Grid] = p.starmap(make_change, work)

    return root_grids + runners


def get_fitness(cost: int, lowest_cost: int, highest_cost: int) -> float:
    """
    Calculates the fitness of a certain root in its generation

    Pre : cost, lowest_cost and highest_cost are integers and lowest_cost is
          lower than highest_cost.
    Post: a float is returned that is between 0 and 1 that represents its
          fitness
    """

    return (highest_cost - cost) / (highest_cost - lowest_cost)


def get_n_changes(fitness: float, max_changes: int, min_changes: int) -> int:
    """
    Gets the 'distance' of the PPA runner, represented by the amount of changes
    from the parent root.

    Pre : type hints are met and min_changes < max_changes
    Post: an integer is returned that is at least min_changes and at most
          max_changes
    """

    return ceil((1 - fitness) * (max_changes - min_changes)) + min_changes


def get_n_runners(fitness: float, max_runners: int, min_runners: int) -> int:
    """
    Gets the amount of runners of the PPA root according to its fitness.

    Pre : type hints are met and min_runners < max_runners
    Post: an integer is returned that is at least min_runenrs and at most
          max_runners
    """

    return ceil(fitness * (max_runners - min_runners)) + min_runners


def make_change(grid: Grid, n_changes: int) -> Grid:
    """
    Makes n_changes changes to the given grid, where a change is swapping the
        connection of two random houses that still give a valid solution.

    Pre : grid is a valid solution with connections and n_changes is a positive
          integer
    Post: a grid is returned with n_changes changes and its cables newly laid
          down according to the new connections
    """

    # make a change n_changes times
    for _ in range(n_changes):
        # find random houses in the grid
        house1, house2 = find_random_houses(grid)

        # perform swap
        swap_houses(house1, house2)

        # remove and then lay the cables back
        grid.remove_cables()
        grid.lay_shared_cables()

    return grid


def plot_results(costs: list[int], grid: Grid, n_generations: int) -> None:
    """
    Plots the best results of each generation.

    Pre : type hints are met
    Post: a matplotlib window should be shown with the correct plot
    """

    plt.title("Plot of best costs per generation (algorithm: plant" +
              "propagation, district: " +
              f"{grid.district}, generations: {n_generations})")
    plt.plot(costs)
    plt.xlabel("Generation")
    plt.ylabel("Best cost")
