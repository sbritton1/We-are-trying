from ...classes.grid import Grid
from ...classes.house import House
from ...classes.battery import Battery
from ...helper_functions.valid_solution import valid_solution
from ...helper_functions.resolve_error import resolve_error
from ...helper_functions.add_random_connections import add_random_connections
from ...helper_functions.swap_houses import swap_houses
from ...helper_functions.possible_swap import possible_swap
from ...helper_functions.find_random_houses import find_random_houses

import random
import copy
import multiprocessing
import matplotlib.pyplot as plt


def init_hill_climber_shared(grid: Grid) -> Grid:
    """
    Initialises grid 8 times, then plots the results and
    returns the grid with the best solution.

    Pre: grid is of class grid
    Post: returns best found solution using this algorithm
    """

    # create list of grids as work for multithreading
    grids: list[Grid] = []

    # amount of grids to run algorithm on
    for i in range(4):

        # create deepcopy to not mess with original
        tmp_grid = copy.deepcopy(grid)
        tmp_grid = add_random_connections(tmp_grid)

        # make sure the grid already is a valid solution
        while valid_solution(tmp_grid) is False:
            resolve_error(tmp_grid)

        tmp_grid.lay_shared_cables()
        # tmp_grid.remove_cables()

        grids.append(tmp_grid)

    # use multithread processing, with workers amount of threads
    workers = 4
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
    Pre: grid of class grid
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
    This is an algorithm for shared cables and it uses the
    hill climber method. This algorithm will be done a few
    times, to try to negate the randomness effect.
    Pre: grid is a class of grid
    Post: grid is a class of grid
    """

    tmp_grid = copy.deepcopy(grid)

    costs = []

    best_cost = 10000000

    # initialize stop conditions
    times_no_improvement = 0
    max_iterations = 0

    while times_no_improvement < 500 and max_iterations < 500:
        
        # changes grid in random places
        a_grid, new_cost = change_grid_hill_climber(tmp_grid, best_cost)

        # condition that checks if it is an improved solution
        if new_cost < best_cost:
            times_no_improvement = 0
            best_cost = new_cost
            tmp_grid = a_grid
        else:
            times_no_improvement += 1

        max_iterations += 1

        costs.append(best_cost)

    return tmp_grid, costs


def change_grid_hill_climber(grid: Grid, best_cost: int):
    """
    This function tries n times to connect two different houses with two
    different batteries, to improve the current grid.
    Pre: grid is of class grid and best_cost is an integer
    Post: returns list with 3 items, where the first item is a bool item
          that refers to improvement of the grid. The second item is the new cost
          as integer. The final item is the new optimised grid
    """


    tmp_grid = copy.deepcopy(grid)
    tmp_grid.remove_cables()

    # tries 20 times to change houses with batteries
    for _ in range(1):
        grid = copy.deepcopy(tmp_grid)

        house_1, house_2 = find_random_houses(tmp_grid)

        if possible_swap(house_1, house_2):
            swap_houses(house_1, house_2)

    # copy of grid
    test_grid = copy.deepcopy(tmp_grid)

    # lays cables in copy of grid
    for battery in test_grid.batteries:
        battery.lay_shared_cables()

    # costs for the copy of the grid
    cost = test_grid.calc_cost_shared()

    # checks for improvement
    new_grid, new_cost = check_if_improvement(cost, best_cost, test_grid)

    return new_grid, new_cost


def find_random_houses(grid: Grid) -> list[House, House]:
    """
    Chooses two random houses from all houses in the grid and checks
    if they are not connected to the same battery.
    Pre: grid is of class Grid
    Post: returns two different houses as house object
    """
    house_1 = random.choice(grid.houses)
    house_2 = random.choice(grid.houses)

    # chooses new houses if they are connected to the same battery
    while house_1 is house_2 and house_1.connection is house_2.connection:
        house_1 = random.choice(grid.houses)
        house_2 = random.choice(grid.houses)

    return house_1, house_2


def check_if_improvement(cost: int, best_cost: int, grid: Grid):
    """
    Checks if the new configuration of the houses gives an improved solution for the grid
    and it also checks if it is a valid solution.
    Pre: The cost and best_cost are integers, and grid is of class Grid
    Post: returns list with 3 items, where the first item is a bool item
          that refers to improvement of the grid. The second item is the new cost
          as integer. The final item is the new optimised grid
    """
    # checks if the cost is lower than the previous costs and also checks if it is a valid solution
    if cost < best_cost and valid_solution(grid):
        return grid, cost
    else:
        return grid, best_cost


def plot_costs_graph(costs: list[int], district: str) -> None:
    """
    Plots a graph of all the costs from the random solutions.
    Pre: list of integers
    Post: none
    """

    iterations = list(range(len(costs)))
    plt.plot(iterations, costs)
    plt.title(f"Graph of cost over time from simulated annealing algorithm\nDistrict: {district}")
    plt.xlabel("Iteration")
    plt.ylabel("Cost")
    plt.show()