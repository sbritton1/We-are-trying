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
import matplotlib.pyplot as plt


def init_hill_climber_shared(grid: Grid, fill: bool = True) -> Grid:
    """
    Initialises grid 8 times, then plots the results and
    returns the grid with the best solution.

    Pre:  grid is of class grid
    Post: returns best found solution using this algorithm
    """

    # create list of grids as work for multithreading
    grids: list[Grid] = []

    # amount of grids to run algorithm on
    for i in range(6):

        # create deepcopy to not mess with original
        tmp_grid = copy.deepcopy(grid)

        if fill is True:
            tmp_grid = add_random_connections(tmp_grid)

            # make sure the grid already is a valid solution
            while valid_solution(tmp_grid) is False:
                resolve_error(tmp_grid)

            tmp_grid.lay_shared_cables()

        grids.append(tmp_grid)

    # use multithread processing, with workers amount of threads
    workers = 6
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

    # graph how cost has decreased over time from algorithm
    plot_costs_graph(costs_best_solution, best_solution.district)

    best_solution.remove_cables()
    return best_solution


def work(tmp_grid: Grid) -> tuple[Grid, int]:
    """
    Runs the simulated annealing and returns the
    grid and costs.

    Pre:  grid of class grid
    Post: tuple containing grid of class grid and integer
    """

    # run algorithm and return the result
    run_algo = hill_climber_shared(tmp_grid)
    tmp_grid: Grid = run_algo[0]
    costs = run_algo[1]
    print(tmp_grid.cost)
    return (tmp_grid, costs)


def hill_climber_shared(grid: Grid) -> Grid:
    """
    This is an algorithm for shared cables and it uses the hill climber
    method. This algorithm will be done a few times, to try to negate
    the randomness effect.

    Pre:  grid is a class of grid
    Post: grid is a class of grid
    """

    tmp_grid: Grid = copy.deepcopy(grid)

    # list that contains all costs over all iterations
    costs: list[int] = []

    # the cost of the current grid is the initialized cost
    best_cost: int = tmp_grid.calc_cost_shared()

    # initialize stop conditions
    times_no_improvement: int = 0
    max_iterations: int = 0

    while times_no_improvement < 700 and max_iterations < 15000:

        # changes grid in random places
        grid_and_cost: tuple(Grid, int) = change_grid_hill_climber(tmp_grid, best_cost)

        # condition that checks if it is an improved solution
        if grid_and_cost[1] < best_cost:
            times_no_improvement = 0
            best_cost = grid_and_cost[1]
            tmp_grid = grid_and_cost[0]
        else:
            times_no_improvement += 1

        max_iterations += 1

        # saves new cost in cost list
        costs.append(best_cost)

    return tmp_grid, costs


def change_grid_hill_climber(grid: Grid, best_cost: int):
    """
    This function tries n times to connect two different houses with two
    different batteries, to improve the current grid.

    Pre:  grid is of class grid and best_cost is an integer
    Post: returns list with 3 items, where the first item is a bool item
          that refers to improvement of the grid. The second item is the new
          cost as integer. The final item is the new optimised grid
    """

    tmp_grid: Grid = copy.deepcopy(grid)
    tmp_grid.remove_cables()

    # gets two random houses
    houses: tuple(House, House) = find_random_houses(tmp_grid)

    # swaps two houses if possible
    if possible_swap(houses[0], houses[1]):
        swap_houses(houses[0], houses[1])

    # copy of grid
    test_grid: Grid = copy.deepcopy(tmp_grid)

    # lays cables in copy of grid
    for battery in test_grid.batteries:
        battery.lay_shared_cables()

    # costs for the copy of the grid
    cost: int = test_grid.calc_cost_shared()

    # checks for improvement
    grid_and_cost: tuple(Grid, int) = check_if_improvement(cost, best_cost, test_grid)

    return grid_and_cost[0], grid_and_cost[1]


def check_if_improvement(cost: int, best_cost: int, grid: Grid):
    """
    Checks if the new configuration of the houses gives an improved
    solution for the grid and it also checks if it is a valid solution.

    Pre:  the cost and best_cost are integers, and grid is of class Grid
    Post: returns list with 3 items, where the first item is a bool item
          that refers to improvement of the grid. The second item is the
          new cost as integer. The final item is the new optimised grid
    """

    # checks if cost is lower than previous costs
    if cost < best_cost:
        return grid, cost
    else:
        return grid, best_cost


def plot_costs_graph(costs: list[int], district: str) -> None:
    """
    Plots a graph of all the costs from the random solutions.

    Pre : list of integers
    Post: none
    """

    iterations: list[int] = list(range(len(costs)))
    plt.plot(iterations, costs)
    plt.title(f"Graph of cost over time from hill climber algorithm\n \
              District: {district}")
    plt.xlabel("Iteration")
    plt.ylabel("Cost")
    plt.show()
