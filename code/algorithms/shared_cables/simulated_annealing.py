from ...classes.grid import Grid
from ...helper_functions.valid_solution import valid_solution
from ...helper_functions.resolve_error import resolve_error
from ...helper_functions.add_random_connections import add_random_connections
from ...helper_functions.find_random_houses import find_random_houses
from ...helper_functions.swap_and_replace_cables import swap_and_replace_cables
import matplotlib.pyplot as plt
import random
import copy
import multiprocessing
import math


def init_simulated_annealing(grid: Grid) -> Grid:
    """
    Initialises random grids and runs simulated annealing algorithm
    on them using multiple threads.

    Pre : grid is of class grid
    Post: returns best found solution using this algorithm
    """

    # create list of grids as work for multithreading
    grids: list[Grid] = []

    # amount of grids to run algorithm on
    n_grids = 50

    # amount of grids to run algorithm on
    for _ in range(n_grids):

        # create deepcopy to not mess with original
        tmp_grid: Grid = copy.deepcopy(grid)
        tmp_grid = add_random_connections(tmp_grid)

        # make sure the grid already is a valid solution
        while valid_solution(tmp_grid) is False:
            resolve_error(tmp_grid)

        tmp_grid.lay_shared_cables()

        grids.append(tmp_grid)

    # use multithread processing, with workers = amount of threads
    workers: int = 8
    p = multiprocessing.Pool(workers)
    results: tuple(Grid, int) = (p.map(simulated_annealing, grids))

    best_solution: Grid = analyze_results(results)

    best_solution.remove_cables()

    return best_solution


def simulated_annealing(grid: Grid) -> tuple[Grid, list[int]]:
    """
    Simulated annealing algorithm, which is a hill climber that has a
    chance to accept negative changes based on a temperature function.

    Pre : grid of class grid
    Post: tuple containing grid of class grid and list of integers,
          where the list of integers is the cost history of the grid
    """

    # store current cost of the grid
    org_cost = grid.calc_cost_shared()
    cost_grid: int = org_cost
    costs: list[int] = []
    last_update: int = 0

    # try a maximum of n_iterations of swaps
    n_iterations = 15000

    for iteration in range(n_iterations):

        # create deepcopy to make temporary changes
        tmp_grid: Grid = copy.deepcopy(grid)

        # get two random houses not connected to the same battery
        house1, house2 = find_random_houses(tmp_grid)

        swap_and_replace_cables(house1, house2)
        new_cost: int = tmp_grid.calc_cost_shared()

        # if new cost is lower, accept the change
        if pass_change(cost_grid, new_cost, iteration) is True:
            grid = tmp_grid
            cost_grid = new_cost
            last_update = iteration

        # break if no more improvements have been found in a while
        if iteration - last_update == 500:
            break

        costs.append(cost_grid)

    print(grid.cost)

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

    # always accept a positive change
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


def analyze_results(results: list[tuple[Grid, list[int]]]) -> Grid:
    """
    Looks through all the results to find the best solution. Then plots
    a graph of the cost history of the best solution.

    Pre : results is a list of tuples of Grid and a list of ints
    Post: plots graph of cost history of best solution and returns
          Grid of best solution
    """

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

        # check if this cost is lowest yets
        if lowest_cost is None or tmp_grid.cost < lowest_cost:
            costs_best_solution = costs
            lowest_cost = tmp_grid.cost
            best_solution = tmp_grid

    print(all_costs)
    plot_costs_graph(costs_best_solution, best_solution.district)

    return best_solution


def plot_costs_graph(costs: list[int], district: str) -> None:
    """
    Plots a graph of the cost over time of the best solution from
    the simulated annealing algorithm.

    Pre : list of integers
    Post: graph of cost over time is plotted
    """

    iterations: list[int] = list(range(len(costs)))
    plt.plot(iterations, costs)
    plt.title("Graph of cost over time from simulated annealing algorithm\n" +
              f"District: {district}, Cost: {costs[-1]}")
    plt.xlabel("Iteration")
    plt.ylabel("Cost")
