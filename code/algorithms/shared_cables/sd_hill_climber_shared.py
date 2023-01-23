from ...classes.grid import Grid
from ...classes.house import House
from ...classes.battery import Battery
from ...helper_functions.valid_solution import valid_solution
from ...helper_functions.resolve_error import resolve_error
from ...helper_functions.add_random_connections import add_random_connections
import random
import copy
import math
import multiprocessing


def init_sd_hill_climber_shared(grid: Grid) -> Grid:
    """
    Initializes grids for the steepest descent hill climber
    to improve, optimized for shared cables

    Pre : grid is of class Grid
    Post: returns best found solution using this algorithm
    """

    # keeps track of costs of all solutions
    lowest_cost: int = None
    best_solution: Grid = None

    # how many random grids to run algorithm on
    for i in range(1):

        # create deepcopy and fill in randomly
        tmp_grid: Grid = copy.deepcopy(grid)
        tmp_grid = add_random_connections(tmp_grid)

        # if solution is not valid, make it so
        while valid_solution(tmp_grid) is False:
            resolve_error(tmp_grid)

        # run steepest descent hill climber algorithm
        tmp_grid = sd_hill_climber_shared(tmp_grid)

        cost: int = tmp_grid.calc_cost_shared()

        # check if solution is cheepest found
        if lowest_cost is None or cost < lowest_cost:
            lowest_cost = cost
            best_solution = tmp_grid

    best_solution.remove_cables()
    return best_solution


def sd_hill_climber_shared(grid: Grid) -> Grid:
    """
    Steepest descent hill climber algorithm

    Pre : Grid is of class Grid
    Post: returns grid with all improvements applied
    """

    grid.lay_shared_cables()

    while True:
        print(grid.calc_cost_shared())

        # decide how many threads to use
        workers = 4

        # create list of work to process
        work = []
        for worker_id in range(workers):
            work.append((grid, worker_id, workers))

        # create processing pool and apply it
        p = multiprocessing.Pool(workers)
        results = (p.starmap(try_combinations, work))

        # find the best improvement made
        best_improvement: int = 0
        best_grid: Grid = None
        for result in results:
            new_grid: Grid = result[0]
            improvement: int = result[1]
            if improvement > best_improvement:
                best_improvement = improvement
                best_grid = new_grid

        if best_improvement == 0:
            return grid
        
        grid = best_grid


def try_combinations(grid: Grid, id, workers) -> tuple[Grid, int]:

    # create temporary deepcopy of original grid
    tmp_grid = copy.deepcopy(grid)
    best_cost = tmp_grid.calc_cost_shared()

    # divide all houses up in chunks, based on amount of workers
    chunk_size = math.ceil(len(tmp_grid.houses) / workers)
    houses_chunked: list[list[House]] = [tmp_grid.houses[i:i + chunk_size] for i in range(0, len(tmp_grid.houses), chunk_size)]

    # select own work based on id of worker
    own_work: list[House] = houses_chunked[id]

    # keep track of best improvement in this segment
    best_improvement: int = 0
    target1: House = None
    target2: House = None

    # try each possible combination
    for house1 in own_work:
        for house2 in tmp_grid.houses:
            if house1.connection != house2.connection:

                # if swap is possible, calculate its improvement
                if possible_swap(house1, house2) is True:
                    improvement = calc_improvement(tmp_grid, best_cost, house1, house2)
                    if improvement > best_improvement:
                        best_improvement = improvement
                        target1 = house1
                        target2 = house2

    # catch when target1 and target2 are still None
    if best_improvement == 0:
        pass

    # swap houses
    else:
        swap_houses(target1, target2)
        tmp_grid.remove_cables()
        tmp_grid.lay_shared_cables()

    # after each combination has been tried, return
    return tmp_grid, best_improvement


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


def calc_improvement(grid: Grid, org_cost: int, house1: House, house2: House) -> int:
    """
    Calculates improvement by replacing the cables with the houses swapped 
    and comparing it to the original cost. Then swaps houses back.

    Pre : grid is of class Grid, org_cost is an int
          house1 and house2 are of class House
    Post: returns int value for improvement. negative return value means
          the cost after the swap is higher.
    """

    grid.remove_cables()
    swap_houses(house1, house2)
    grid.lay_shared_cables()
    new_cost = grid.calc_cost_shared()
    grid.remove_cables()
    swap_houses(house1, house2)

    return org_cost - new_cost


def swap_houses(house1: House, house2: House):
    """
    Swaps the battery of two houses

    Pre : house1 and house2 are of class House
    Post: battery connection of two houses are swapped
    """

    house1_bat: Battery = house1.connection
    house2_bat: Battery = house2.connection

    # disconnect established connections 
    house1_bat.disconnect_home(house1)
    house1.delete_connection()
    house2_bat.disconnect_home(house2)
    house2.delete_connection()

    # make new connections
    house1_bat.connect_home(house2)
    house2.make_connection(house1_bat)
    house2_bat.connect_home(house1)
    house1.make_connection(house2_bat)