import matplotlib.pyplot as plt
import copy
import multiprocessing

from ...classes.grid import Grid
from ...helper_functions.valid_solution import valid_solution
from ...helper_functions.add_random_connections import add_random_connections


def init_baseline_shared(grid: Grid) -> Grid:
    """
    Creates a baseline for what cost we can expect, based on what
    the cost would be if the houses are randomly connected to batteries
    using shared cables.

    Pre : grid is of class Grid
    Post: returns lowest cost solution as Grid
    """

    # set the amount of times a random grid is created
    iterations: int = 10000

    # amount of threads used for multiprocessing
    workers: int = 4

    # use multiprocessing to get the results
    work = [grid] * iterations
    p = multiprocessing.Pool(workers)
    results: list[tuple[Grid, int]] = (p.map(baseline_shared, work))

    # analyze all the results to find the best grid and the costs of
    # all solutions
    final_results = analyze_results(results)
    best_solution = final_results[0]
    costs = final_results[1]

    plot_cost(costs, best_solution, iterations)

    # remove cables before returning
    best_solution.remove_cables()

    return best_solution


def baseline_shared(grid: Grid) -> tuple[Grid, int]:
    """
    Creates a baseline for what cost we can expect, based on what
    the cost would be if the houses are randomly connected to batteries
    and when cables can be shared.

    Pre : grid is of class Grid
    Post: returns a randomly connected grid with shared cables without checking
          if the solution is valid
    """

    # create temporary grid and add random connections
    tmp_grid: Grid = copy.deepcopy(grid)
    tmp_grid = add_random_connections(tmp_grid)

    # lay cables and calculate the cost
    tmp_grid.lay_shared_cables()
    cost: int = tmp_grid.calc_cost_shared()

    return tmp_grid, cost


def analyze_results(results: list[tuple[Grid, int]]) -> tuple[Grid, list[int]]:
    """
    Looks through results, stores final cost of each solution
    and stores best found solution.

    Pre : results is a list of a tuple of a grid and an int
    Post: returns tuple of Grid and list of ints, where grid is the
          best solution and list of ints is list of cost of all solutions
    """

    costs = []
    lowest_cost: int = None
    best_solution: Grid = None

    for result in results:
        tmp_grid = result[0]
        cost = result[1]

        # store only valid solutions
        if valid_solution(tmp_grid) is True:
            costs.append(cost)

            # track if new solution is cheapest yet
            if lowest_cost is None or cost < lowest_cost:
                lowest_cost = cost
                best_solution = tmp_grid

    return best_solution, costs


def plot_cost(costs: list[int], grid: Grid, n_iterations: int) -> None:
    """
    Plots a histogram of the costs of all solutions.

    Pre : costs is a list of ints
    Post: displays histogram of all costs of valid solutions
    """

    plt.title("Histogram of costs (algorithm:"
              f"baseline, district: {grid.district}, "
              f"iterations: {n_iterations}, valid solutions: {len(costs)})")
    plt.hist(costs, 20, facecolor='blue', alpha=0.5)
    plt.xlabel("Cost")
    plt.ylabel("Frequency")
