import random
import matplotlib.pyplot as plt
from ...classes.grid import Grid
from ...classes.house import House
from ...classes.battery import Battery
from ...helper_functions.valid_solution import valid_solution
import random
import copy

def baseline(grid: Grid) -> Grid:
    """
    Creates a baseline for what cost we can expect, based on what
    the cost would be if the houses are randomly connected to batteries.
    Pre: grid is of class Grid
    Post: returns lowest cost solution
    """

    # set the amount of iterations
    n_iterations = 1000

    # keeps track of costs of all solutions
    costs: list[int] = []
    best_solution: Grid = grid

    for _ in range(n_iterations):

        # create a temporary grid, all houses are connected to random battery
        tmp_grid: Grid = add_connections(grid)
        cost: int = tmp_grid.calc_cost_normal()

        # add cost if it was a valid solution
        if valid_solution(tmp_grid):
            costs.append(cost)
            
            # check if the solution is the best solution
            if min(costs) == cost:
                best_solution = tmp_grid

    # make histogram of costs of all solutions
    plot_cost(costs, grid, n_iterations)

    return best_solution


def add_connections(grid: Grid) -> Grid:
    """
    Connects houses to random batteries.
    Pre: grid is of class Grid
    Post: returns a copy of original grid, in which
          houses are randomly connected to a battery
    """

    # create deepcopy of original grid
    tmp_grid = copy.deepcopy(grid)

    for house in tmp_grid.houses:

        # loops until available battery is found
        for i in range(len(tmp_grid.batteries)):
            random.shuffle(tmp_grid.batteries)

            # select random battery
            battery = tmp_grid.batteries[i]

            # if battery has enough capacity left, make connection
            if battery.is_connection_possible(house) is True:
                battery.connect_home(house)
                house.make_connection(battery)
                break

    return tmp_grid


def plot_cost(costs: list[int], grid: Grid, n_iterations: int):
    """
    Plots a histogram of the costs of all solutions.
    Pre: costs is a list of ints
    Post: displays histogram
    """
    
    plt.title(f"Histogram of costs (algorithm: baseline, district: {grid.district}, iterations: {n_iterations}, valid solutions: {len(costs)})")
    plt.hist(costs, 20, facecolor='blue', alpha=0.5)
    plt.xlabel("Cost")
    plt.ylabel("Frequency")
    plt.show()

