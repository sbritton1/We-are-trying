from ...classes.grid import Grid
from ...classes.house import House
from ...classes.battery import Battery
from ...helper_functions.valid_solution import valid_solution
from ...helper_functions.resolve_error import resolve_error
from ...helper_functions.add_random_connections import add_random_connections
import random
import copy


def hill_climber_shared(grid: Grid) -> Grid:
    """
    This is an algorithm for shared cables and it uses the
    hill climber method. This algorithm will be done a few
    times, to try to negate the randomness effect.
    
    Pre: grid is a class of grid
    Post: grid is a class of grid   
    """
    
    best_grids = []
    best_costs = []
    
    for _ in range(5):   
        # creates random grid
        tmp_grid = add_random_connections(grid)

        # makes random grid valid
        while valid_solution(tmp_grid) is False:
            resolve_error(tmp_grid)
        
        # artificial best cost which will always be improved
        best_cost = 10000000
        
        # initialize stop conditions
        times_no_improvement = 0
        max_iterations = 0

        while times_no_improvement < 200 and max_iterations < 5000:
            print(max_iterations) 
            
            # changes grid in random places
            changed_grid_and_costs = change_grid_hill_climber(tmp_grid, best_cost)
            
            # condition that checks if it is an improved solution
            if changed_grid_and_costs[0]:
                times_no_improvement = 0
                best_cost = changed_grid_and_costs[1]
                tmp_grid = changed_grid_and_costs[2]
            else:
                times_no_improvement += 1

            max_iterations += 1
            
        # saves 
        best_grids.append(tmp_grid)
        best_costs.append(best_cost)
        
    # print functions to test if algorithm works
    print("\n\n")
    print(best_costs)
    
    # chooses best grid
    min = best_costs[0]
    index = 0
    for i in range(1,len(best_costs)):
        if best_costs[i] < min:
            min = best_costs[i]
            index = i
            
    tmp_grid = best_grids[index]

    return tmp_grid

    
def change_grid_hill_climber(tmp_grid: Grid, best_cost: int) -> list[bool, int, Grid]:
    """
    This function tries n times to connect two different houses with two
    different batteries, to improve the current grid. 
    
    Pre: grid is of class grid and best_cost is an integer
    Post: returns list with 3 items, where the first item is a bool item
          that refers to improvement of the grid. The second item is the new cost
          as integer. The final item is the new optimised grid
    """
    # tries 20 times to change houses with batteries
    for _ in range(20):
        grid = copy.deepcopy(tmp_grid)
        
        house_1, house_2 = find_random_houses(grid)    
            
        battery1 = house_1.connection
        
        battery2 = house_2.connection
        
        swap_houses(house_1, house_2, battery1, battery2)   
    
    # copy of grid
    test_grid = copy.deepcopy(grid)
    
    # lays cables in copy of grid
    for battery in test_grid.batteries:
        battery.lay_shared_cables()
        
    # costs for the copy of the grid
    cost = test_grid.calc_cost_shared()
    
    # checks for improvement
    new_cost = check_if_improvement(cost, best_cost, grid)
    
    return new_cost
    
    
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


def check_if_improvement(cost: int, best_cost: int, grid: Grid) -> list[bool, int, Grid]:
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
        return [True, cost, grid]
    else:
        return [False, best_cost, grid]
    
# mogelijke verbetering: pas deleten wanneer connectie mogelijk
def swap_houses(house_1: House, house_2: House, battery1: Battery, battery2: Battery) -> None:
    """
    Swaps two houses if it does not overflow the capacity of the batteries.
    
    Pre: two houses of the house object, two batteries of the battery object
    Post: it does not return anything
    """
    # deletes connections houses with batteries
    house_1.delete_connection()
    house_2.delete_connection()
    
    battery1.disconnect_home(house_1)
    battery2.disconnect_home(house_2)
    
    # swaps houses if it does not overflow the capacity of the batteries
    if battery1.is_connection_possible(house_2) and battery2.is_connection_possible(house_1):
        house_1.make_connection(battery2)
        house_2.make_connection(battery1)
        
        battery1.connect_home(house_2)
        battery2.connect_home(house_1)
    else:
        house_1.make_connection(battery1)
        house_2.make_connection(battery2)
        
        battery1.connect_home(house_1)
        battery2.connect_home(house_2)
