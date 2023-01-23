from ...classes.grid import Grid
from ...classes.house import House
from ...classes.battery import Battery
from ...helper_functions.valid_solution import valid_solution
from ...helper_functions.resolve_error import resolve_error
from ...helper_functions.add_random_connections import add_random_connections
import matplotlib.pyplot as plt
import random
import copy
import multiprocessing


def init_simulated_annealing(grid: Grid) -> Grid:
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
    run_algo = simulated_annealing(tmp_grid)
    tmp_grid: Grid = run_algo[0]
    costs = run_algo[1]
    print(tmp_grid.cost)
    return (tmp_grid, costs)


def simulated_annealing(grid: Grid) -> tuple[Grid, list[int]]:
    """
    Simulated annealing.
    
    Pre: grid of class grid
    Post: tuple containing grid of class grid and list of integers
    """

    # store current cost of the grid
    cost_grid = grid.calc_cost_shared()
    costs = []
    last_update = 0

    for iteration in range(1000):

        # create deepcopy to make temporary changes
        tmp_grid = copy.deepcopy(grid)

        # get two random houses not connected to the same battery
        while True:
            house1: House = random.choice(tmp_grid.houses)
            house2: House = random.choice(tmp_grid.houses)
            while house2.connection == house1.connection:
                house2: House = random.choice(tmp_grid.houses)

            if possible_swap(house1, house2) is True:
                break
        
        swap_houses(house1, house2)
        
        # lay cables again now that houses are swapped
        tmp_grid.remove_cables()
        tmp_grid.lay_shared_cables()
        new_cost = tmp_grid.calc_cost_shared()

        # if new cost is lower, accept the change
        if new_cost < cost_grid:
            grid = tmp_grid
            cost_grid = new_cost
            last_update = iteration

        # else use temperature function to calculate odds of accepting negative change
        else:

            # create chance of acceptance based on cost difference and iteration
            temperature = 1000 * (0.997 ** iteration)
            acceptation_chance = 2 ** ((cost_grid - new_cost) / temperature)
            if acceptation_chance > random.random():
                grid = tmp_grid
                cost_grid = new_cost
                last_update = iteration

        # break if no more improvements have been found in a while
        if iteration - last_update == 300:
            break

        costs.append(cost_grid)

    return grid, costs


def possible_swap(house1: House, house2: House) -> bool:
    """
    Checks if it is possible to swap two houses based on the
    remaining capacity of their batteries.
    
    Pre: house1 and house2 are of class House
    Post: returns True if houses can be swapped
          else returns False
    """

    if house1.maxoutput > house2.maxoutput + house2.connection.current_capacity:
        return False

    elif house2.maxoutput > house1.maxoutput + house1.connection.current_capacity:
        return False

    return True


def swap_houses(house1: House, house2: House) -> None:
    """
    Swaps the battery of two houses

    Pre : house1 and house2 are of class House
    Post: battery connection of two houses are swapped
    """

    house1_bat: Battery = house1.connection
    house2_bat: Battery = house2.connection

    # remove original connections
    house1_bat.disconnect_home(house1)
    house1.delete_connection()
    house2_bat.disconnect_home(house2)
    house2.delete_connection()

    # create the new connections
    house1_bat.connect_home(house2)
    house2.make_connection(house1_bat)
    house2_bat.connect_home(house1)
    house1.make_connection(house2_bat)


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