import matplotlib.pyplot as plt
import copy

from ...classes.grid import Grid
from ...helper_functions.valid_solution import valid_solution
from ...helper_functions.add_random_connections import add_random_connections


def baseline(grid: Grid) -> Grid:
    """
    Creates a baseline for what cost we can expect, based on what
    the cost would be if the houses are randomly connected to batteries.

    Pre : grid is of class Grid
    Post: returns lowest cost solution
    """

    # set the amount of iterations
    n_iterations: int = 1000

    # keeps track of costs of all solutions
    costs: list[int] = []
    best_solution: Grid = grid

    for _ in range(n_iterations):
        # create a temporary grid
        tmp_grid: Grid = copy.deepcopy(grid)

        # connect all houses to a random battery
        tmp_grid: Grid = add_random_connections(tmp_grid)

        cost: int = tmp_grid.calc_cost_normal()

        # add cost if it was a valid solution
        if valid_solution(tmp_grid) is True:
            costs.append(cost)

            # check if the solution is the best solution
            if min(costs) == cost:
                best_solution = tmp_grid

    # make histogram of costs of all solutions
    plot_cost(costs, grid, n_iterations)

    return best_solution


def plot_cost(costs: list[int], grid: Grid, n_iterations: int) -> None:
    """
    Plots a histogram of the costs of all solutions.

    Pre : costs is a list of ints
    Post: displays histogram
    """

    plt.title("Histogram of costs (algorithm: baseline, district: "
              f"{grid.district}, iterations: {n_iterations}, "
              f"valid solutions: {len(costs)})")
    plt.hist(costs, 20, facecolor='blue', alpha=0.5)
    plt.xlabel("Cost")
    plt.ylabel("Frequency")
