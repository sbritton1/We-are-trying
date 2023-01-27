from ...classes.grid import Grid
from ...helper_functions.valid_solution import valid_solution
from ...helper_functions.add_random_connections import add_random_connections
import matplotlib.pyplot as plt
import copy
import multiprocessing


def init_baseline_shared(grid: Grid) -> Grid:
    """
    Creates a baseline for what cost we can expect, based on what
    the cost would be if the houses are randomly connected to batteries
    using shared cables.

    Pre:  grid is of class Grid
    Post: returns lowest cost solution as Grid
    """

    iterations: int = 100000

    workers: int = 8
    work = [grid] * iterations
    p = multiprocessing.Pool(workers)
    results: tuple[list[Grid], int] = (p.map(baseline_shared, work))

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

    plot_cost(costs, best_solution, iterations)

    best_solution.remove_cables()
    return best_solution


def baseline_shared(grid: Grid) -> tuple[Grid, int]:
    """
    Creates a baseline for what cost we can expect, based on what
    the cost would be if the houses are randomly connected to batteries
    and when cables can be shared.

    Pre : grid is of class Grid
    Post: returns lowest cost solution
    """

    # create temporary grid and add random connections
    tmp_grid: Grid = copy.deepcopy(grid)
    tmp_grid = add_random_connections(tmp_grid)

    # lay cables and calculate the cost
    tmp_grid.lay_shared_cables()
    cost: int = tmp_grid.calc_cost_shared()

    return tmp_grid, cost


def plot_cost(costs: list[int], grid: Grid, n_iterations: int) -> None:
    """
    Plots a histogram of the costs of all solutions.
    
    Pre : costs is a list of ints
    Post: displays histogram
    """

    plt.title(f"Histogram of costs (algorithm: baseline, district: {grid.district}, " + \
              f"iterations: {n_iterations}, valid solutions: {len(costs)})")
    plt.hist(costs, 20, facecolor='blue', alpha=0.5)
    plt.xlabel("Cost")
    plt.ylabel("Frequency")
    plt.show()
