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

    Pre : grid is of class grid
    Post: returns best found solution using this algorithm
    """
        
    # create list of grids as work for multithreading
    n_grids: int = 4
    grids: list[Grid] = []
    
    grids = get_grids(n_grids, grids, grid, fill)

    # use multithread processing, with workers amount of threads
    workers: int = 4
    p = multiprocessing.Pool(workers)
    results = (p.map(hill_climber_shared, grids))

    best_solution: Grid = get_best_solution(results)

    # graph how cost has decreased over time from algorithm    
    # plot_costs_graph(costs_best_solution, best_solution.district)
    
    best_solution.remove_cables()
    return best_solution


def get_best_solution(results: tuple[Grid, list[int]]) -> Grid:
    """
    Gets the best solutions from all the runs.
    
    Pre : a tuple containing a grid and a list of integers
    Post: tuple containing list of integers, integer and a Grid 
    """
    
    lowest_cost: int = None
    best_solution: Grid = None
    for result in results:
        tmp_grid: Grid = result[0]
        if lowest_cost is None or tmp_grid.cost < lowest_cost:
            lowest_cost = tmp_grid.cost
            best_solution = tmp_grid
        
    return best_solution


def get_grids(n_grids: int, grids: list[Grid], grid: Grid, fill: bool) -> list[Grid]:
    """
    Gets n grids on which hill climber can be used.
    
    Pre : integer and list of grids
    Post: list of grids
    """
    for i in range(n_grids):
        # create deepcopy to not mess with original
        tmp_grid: Grid = copy.deepcopy(grid)
        
        if fill is True:
            tmp_grid = greedy(tmp_grid)

            # make sure the grid already is a valid solution
            while valid_solution(tmp_grid) is False:
                resolve_error(tmp_grid)

            tmp_grid.lay_shared_cables()

        grids.append(tmp_grid)
    
    return grids


def hill_climber_shared(grid: Grid) -> tuple[Grid, list[int]]:
    """
    This is an algorithm for shared cables and it uses the hill climber
    method. This algorithm will be done a few times, to try to negate
    the randomness effect.

    Pre : grid is a class of grid
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
        grid_and_cost: tuple[Grid, int] = change_grid_hill_climber(tmp_grid, best_cost)

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

    print(tmp_grid.cost)
    return tmp_grid, costs


def change_grid_hill_climber(grid: Grid, best_cost: int) -> tuple[Grid, int]:
    """
    This function tries n times to connect two different houses with two
    different batteries, to improve the current grid.

    Pre : grid is of class grid and best_cost is an integer
    Post: tuple containing grid of class Grid and integer as cost
    """

    tmp_grid: Grid = copy.deepcopy(grid)

    # gets two random houses
    houses: tuple[House, House] = find_random_houses(tmp_grid)
    
    # removes cables  from selected batteries
    houses[0].connection.remove_cables()
    houses[1].connection.remove_cables()

    # swaps two houses if possible
    if possible_swap(houses[0], houses[1]):
        swap_houses(houses[0], houses[1])

    # lays cables again
    houses[0].connection.lay_shared_cables()
    houses[1].connection.lay_shared_cables()

    # costs for the copy of the grid
    cost: int = tmp_grid.calc_cost_shared()

    # checks for improvement
    new_cost: int = check_if_improvement(cost, best_cost)

    return tmp_grid, new_cost


def check_if_improvement(cost: int, best_cost: int) -> int:
    """
    Checks if the new configuration of the houses gives an improved
    solution for the grid and it also checks if it is a valid solution.

    Pre : the cost and best_cost are integers
    Post: integer
    """

    # checks if cost is lower than previous costs
    if cost < best_cost:
        return cost
    else:
        return best_cost


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
