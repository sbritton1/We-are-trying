from ...classes.grid import Grid
from ...classes.house import House
from ...helper_functions.valid_solution import valid_solution
from ...helper_functions.resolve_error import resolve_error
from ...helper_functions.add_random_connections import add_random_connections
from ...helper_functions.possible_swap import possible_swap
from ...helper_functions.swap_houses import swap_houses
from ...helper_functions.find_random_houses import find_random_houses
from ..own_cables.greedy import greedy
import matplotlib.pyplot as plt
import random
import copy
import multiprocessing
import math


def init_simulated_annealing(grid: Grid) -> Grid:
    """
    Initialises random grids and runs simulated annealing algorithm
    on them using multiple threads.

    Pre: grid is of class grid
    Post: returns best found solution using this algorithm
    """

    # create list of grids as work for multithreading
    grids: list[Grid] = []

    # amount of grids to run algorithm on
    for i in range(4):

        # create deepcopy to not mess with original
        tmp_grid: Grid = copy.deepcopy(grid)
        tmp_grid = add_random_connections(tmp_grid)

        # make sure the grid already is a valid solution
        while valid_solution(tmp_grid) is False:
            resolve_error(tmp_grid)

        tmp_grid.lay_shared_cables()

        grids.append(tmp_grid)

    # use multithread processing, with workers = amount of threads
    workers: int = 4
    p = multiprocessing.Pool(workers)
    results: tuple(Grid, int) = (p.map(work, grids))

    # keeps track of costs of all solutions
    costs_best_solution: list[int] = []
    lowest_cost: int = None
    best_solution: Grid = None

    all_costs = []

    # loop through results to find best one
    for result in results:
        tmp_grid: Grid = result[0]
        costs: list[int] = result[1]
        all_costs.append(costs[-1])
        if lowest_cost is None or tmp_grid.cost < lowest_cost:
            costs_best_solution = costs
            lowest_cost = tmp_grid.cost
            best_solution = tmp_grid

    # graph how cost has decreased over time from algorithm
    print(all_costs)
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
    run_algo: tuple(Grid, list[int]) = simulated_annealing(tmp_grid)
    tmp_grid: Grid = run_algo[0]
    costs: list[int] = run_algo[1]
    print(tmp_grid.cost)
    return (tmp_grid, costs)


def simulated_annealing(grid: Grid) -> tuple[Grid, list[int]]:
    """
    Simulated annealing algorithm.

    Pre: grid of class grid
    Post: tuple containing grid of class grid and list of integers
    """

    # store current cost of the grid
    org_cost = grid.calc_cost_shared()
    cost_grid: int = org_cost
    costs: list[int] = []
    last_update: int = 0

    for iteration in range(15000):

        # create deepcopy to make temporary changes
        tmp_grid: Grid = copy.deepcopy(grid)

        # get two random houses not connected to the same battery
        two_houses: tuple[House, House] = find_random_houses(tmp_grid)
        house1: House = two_houses[0]
        house2: House = two_houses[1]
        
        house1.connection.remove_cables()
        house2.connection.remove_cables()
        swap_houses(house1, house2)

        # lay cables again now that houses are swapped
        house1.connection.lay_shared_cables()
        house2.connection.lay_shared_cables()
        new_cost = tmp_grid.calc_cost_shared()

        # if new cost is lower, accept the change
        if pass_change(cost_grid, new_cost, iteration) is True:
            grid = tmp_grid
            cost_grid = new_cost
            last_update = iteration

        # break if no more improvements have been found in a while
        if iteration - last_update == 500:
            break

        costs.append(cost_grid)

    return grid, costs


def pass_change(org_cost: int, new_cost: int, iteration: int) -> bool:
    """
    Checks if a change should be accepted, based on the new cost
    of the grid, the original cost and a temperature function depending
    on the iteration.

    Pre : org_cost, new_cost and iteration are integers
    Post: returns True if change should be accepted
          else return False
    """

    if new_cost < org_cost:
        return True

    # dont accept changes way over the original grid cost
    elif new_cost > org_cost * 1.1:
        return False

    else:
        temperature = 500 * (0.997 ** iteration) + ((25 / (math.sqrt(int(iteration / 1000)) + 1)) * 0.997 ** (iteration % 1000))
        acceptation_chance = 2 ** ((org_cost - new_cost) / temperature)
        if acceptation_chance > random.random():
            return True


def plot_costs_graph(costs: list[int], district: str) -> None:
    """
    Plots a graph of all the costs from the random solutions.

    Pre: list of integers
    Post: none
    """

    iterations: list[int] = list(range(len(costs)))
    plt.plot(iterations, costs)
    plt.title(f"Graph of cost over time from simulated annealing algorithm\n" + \
              f"District: {district}, Cost: {costs[-1]}")
    plt.xlabel("Iteration")
    plt.ylabel("Cost")
