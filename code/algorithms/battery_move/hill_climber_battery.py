from ...classes.grid import Grid
from ...classes.house import House
from ...classes.battery import Battery
from ...helper_functions.valid_solution import valid_solution
from ...helper_functions.resolve_error import resolve_error
from ...helper_functions.add_random_connections import add_random_connections
from ...helper_functions.swap_houses import swap_houses
from ...helper_functions.possible_swap import possible_swap
from ...helper_functions.find_random_houses import find_random_houses
from ..own_cables.greedy import greedy
import copy
import multiprocessing
import random


def init_hill_climber_battery(grid: Grid):

    # create list of grids as work for multithreading
    grids: list[Grid] = []

    # amount of grids to run algorithm on
    for i in range(1):

        # create deepcopy to not mess with original
        tmp_grid = copy.deepcopy(grid)
        tmp_grid = greedy(tmp_grid)

        tmp_grid.lay_shared_cables()
        tmp_grid.calc_cost_shared()

        grids.append(tmp_grid)

    # use multithread processing, with workers amount of threads
    workers = 1
    p = multiprocessing.Pool(workers)
    results = (p.map(hill_climber_battery, grids))

    best_result: Grid = None
    best_costs: list[int] = []
    for result in results:
        new_grid = result[0]
        costs = result[1]
        if costs[-1] < best_costs[-1]:
            best_costs = costs
            best_result = new_grid

    return best_result


def hill_climber_battery(grid: Grid) -> tuple[Grid, list[int]]:
    org_cost: int = grid.cost
    costs: list[int] = []
    last_improvement: int = 0
    iteration: int = 0

    while iteration - last_improvement < 100 and iteration < 1000:
        print(iteration)
        tmp_grid: Grid = copy.deepcopy(grid)
        tmp_grid.remove_all_connections()
        print("check1")
        move_battery(tmp_grid)
        print("check2")
        tmp_grid = greedy(tmp_grid)
        tmp_grid.lay_shared_cables()
        new_cost = tmp_grid.calc_cost_shared()

        if new_cost < org_cost:
            grid = tmp_grid
            print(new_cost)
            costs.append(new_cost)
            org_cost = new_cost
            last_improvement = iteration
        
        iteration += 1

    print(costs[-1])
    return grid, costs


def move_battery(grid: Grid) -> None:
    """
    Moves battery to different coordinates.
    
    Pre:  grid from Grid class
    Post: none  
    """
    battery = random.choice(grid.batteries)
    # y and x direction
    
    # battery coordinates
    old_x = battery.coord_x        
    old_y = battery.coord_y   
    
    direction = random_direction()
        
    y_direction = 0
    x_direction = direction
        
    y_or_x = random_direction()
    
    # chooses if x or y moves
    if y_or_x == 1:
        y_direction = direction
        x_direction = 0
    
    # new coordinates
    new_x = old_x + x_direction
    new_y = old_y + y_direction
    
    while True:
        if grid.move_battery(battery, new_x, new_y):
            break
        else:
            # when on house, move battery and try again
            direction = random_direction()
        
            y_direction = 0
            x_direction = direction
            
            y_or_x = random_direction()
            
            # chooses if x or y moves
            if y_or_x == 1:
                y_direction = direction
                x_direction = 0 
                
            new_x = old_x + x_direction
            new_y = old_y + y_direction

    
def random_direction() -> int:
    """
    Gets random direction.
    
    Pre:  none
    Post: integer
    """
    
    # coin flip
    direction = random.randint(0,1)
    
    if direction == 0:
        direction = -1
        
    return direction