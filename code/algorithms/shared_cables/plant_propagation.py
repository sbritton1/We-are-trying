from copy import deepcopy
from math import ceil
from random import shuffle

from ...classes.grid import Grid
from ...classes.battery import Battery
from ...classes.house import House
from ...helper_functions.valid_solution import valid_solution
from ...helper_functions.resolve_error import resolve_error
from ...helper_functions.add_random_connections import add_random_connections
from .sd_hill_climber_shared import sd_hill_climber_shared
from .hill_climber_shared import hill_climber_shared

def plant_propagation(grid: Grid) -> Grid:
    
    # * set algorithm parameters
    shared_cables = True
    min_runners = 1
    max_runners = 5
    min_changes = 1
    max_changes = 40
    n_generations = 8

    # make a list to store the temporary grids
    tmp_grids: list[Grid] = []
    
    for _ in range(max_runners):
        tmp_grid: Grid = deepcopy(grid)
        tmp_grid = add_random_connections(tmp_grid)

        while valid_solution(tmp_grid) is False:
            resolve_error(tmp_grid)

        tmp_grid.lay_shared_cables()

        tmp_grids.append(tmp_grid)

    # set 
    root_grids = tmp_grids

    for _ in range(n_generations):
        print(_)
        runners = create_new_generation(root_grids, min_runners,
                                           max_runners, min_changes,
                                           max_changes, shared_cables)
        
        # sort runners in ascending order of cost
        runners.sort(key=lambda x: x.calc_cost_shared())
        
        # set the best runners as the new roots
        root_grids = runners[:max_runners]    

    # choose the best runner of the last generation
    best_runner = runners[0]

    # remove the cables of the best runner
    best_runner.remove_cables()
    
    return best_runner 


def create_new_generation(root_grids: list[Grid], min_runners: int,
                          max_runners: int, min_changes: int, max_changes: int,
                          shared_cables: bool):

    # keeps track of costs of all solutions
    lowest_cost: int = None
    highest_cost: int = None

    # go over each grid and check for the highest and lowest cost
    for root_grid in root_grids:
        cost = calculate_cost(root_grid, shared_cables)
        if lowest_cost is None or cost < lowest_cost:
            lowest_cost = cost
        if highest_cost is None or cost > highest_cost:
            highest_cost = cost

    # determine the fitness and thus how many runners should be created and how
    # far each runner should go
    runners : list[Grid] = []

    for root_grid in root_grids:
        fitness = get_fitness(root_grid.cost, lowest_cost, highest_cost)

        n_runners = get_n_runners(fitness, max_runners, min_runners)

        n_changes = get_n_changes(fitness, max_changes, min_changes)

        print(f"Grid cost: {root_grid.cost}, fitness: {fitness}, n_runners: {n_runners}, n_changes: {n_changes}")

        for _ in range(n_runners):
            runner = deepcopy(root_grid)
            for _ in range(n_changes):
                make_change(runner)

        runners.append(runner)

    return runners


def calculate_cost(grid: Grid, shared_cables: bool) -> int:
    if shared_cables:
        return grid.calc_cost_shared()
    return grid.calc_cost_normal()


def get_fitness(cost: int, lowest_cost: int, highest_cost: int) -> float:
    return (highest_cost - cost) / (highest_cost - lowest_cost)


def get_n_changes(fitness: float, max_changes: int, min_changes: int) -> int:
    return ceil((1 - fitness) * (max_changes - min_changes)) + min_changes


def get_n_runners(fitness: float, max_runners: int, min_runners: int) -> int:
    return ceil(fitness * (max_runners - min_runners)) + min_runners


def make_change(grid: Grid) -> None:
    shuffle(grid.houses)

    # loop through possible swap of houses
    for house1 in grid.houses:
        for house2 in grid.houses:
            if house1.connection != house2.connection:
                
                # check if swap is possible
                if is_possible_swap(house1, house2) is True:
                    # perform swap
                    swap_houses(house1, house2)

                    # remove and then lay the cables back
                    grid.remove_cables()
                    grid.lay_shared_cables()

                    return        


def is_possible_swap(house1: House, house2: House) -> bool:
    """
    Checks if two houses can be swapped by looking at the capacity
    of the batteries and the output of the houses

    Pre : house1 and house2 are of class House
    Post: returns true if houses can be swapped
          else return false    
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

    # disconnects established connections
    house1_bat.disconnect_home(house1)
    house1.delete_connection()
    house2_bat.disconnect_home(house2)
    house2.delete_connection()

    # makes new connections
    house1_bat.connect_home(house2)
    house2.make_connection(house1_bat)
    house2_bat.connect_home(house1)
    house1.make_connection(house2_bat)
  