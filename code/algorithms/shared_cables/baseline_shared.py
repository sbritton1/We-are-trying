from ...classes.grid import Grid
from ...classes.house import House
from ...classes.battery import Battery
from ...helper_functions.valid_solution import valid_solution
from ...helper_functions.resolve_error import resolve_error
import matplotlib.pyplot as plt
import random
import copy


def baseline_shared(grid: Grid) -> Grid:

    # set the amount of iterations
    iterations = 1000

    # keeps track of costs of all solutions
    costs = []
    lowest_cost: int = None
    best_solution: Grid = None

    for i in range(iterations):
        print(i)
        tmp_grid: Grid = copy.deepcopy(grid)
        tmp_grid = add_random_connections(tmp_grid)
        
        tmp_grid.lay_shared_cables()

        cost: int = tmp_grid.calc_cost_shared()

        if valid_solution(tmp_grid) is True:
            costs.append(cost)

            if lowest_cost is None or cost < lowest_cost:
                lowest_cost = cost
                best_solution = tmp_grid

    best_solution.remove_cables()

    plot_cost(costs, best_solution, iterations)
    return best_solution


def add_random_connections(tmp_grid: Grid) -> Grid:
    """
    Connects houses to random batteries.
    Pre: grid is of class Grid
    Post: returns a copy of original grid, in which
          houses are randomly connected to a battery
    """

    for house in tmp_grid.houses:

        # loops until available battery is found
        for i in range(len(tmp_grid.batteries)):
            random.shuffle(tmp_grid.batteries)

            # select random battery
            battery: Battery = tmp_grid.batteries[i]

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
