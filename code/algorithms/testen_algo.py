from ..classes.grid import Grid
from ..classes.house import House
from ..classes.battery import Battery
import random
import copy

def testen_algo(grid: Grid):
    # maak random grid
    tmp_grid = add_connections(grid)   
    
    # maak best cost die altijd verbeterd kan worden 
    best_cost = 10000000
    
    my_condition = 0

    # loop die stopt wanneer 500 keer geen verbetering te zien is
    while my_condition < 500:
        print(my_condition)
        if change_grid_hill_climber(tmp_grid, best_cost)[0]:
            my_condition = 0
            best_cost = change_grid_hill_climber(tmp_grid, best_cost)[1]
            tmp_grid = change_grid_hill_climber(tmp_grid, best_cost)[2]
        else:
            my_condition += 1
            
    return tmp_grid
    
    
def add_connections(grid: Grid) -> Grid:
    """
    Connects houses to random batteries.
    Pre: grid is of class Grid
    Post: returns a copy of original grid, in which
          houses are randomly connected to a battery
    """

    # create deepcopy of original grid
    tmp_grid = copy.deepcopy(grid)

    # ! Hier kunnen we slimmer checken of alle batterijen al zijn gecapped om
    # ! zo minder vaak te checken of alles gecapped is en ook eerder te stoppen

    for house in tmp_grid.houses:

        # loops until available battery is found
        while True:

            # check if any battery has enough capacity left
            if all_batteries_capped(house, tmp_grid.batteries) is True:
                break

            # select random battery
            battery = random.choice(tmp_grid.batteries)

            # if battery has enough capacity left, make connection
            if battery.is_connection_possible(house) is True:
                battery.connect_home(house)
                house.make_connection(battery)
                break

    return tmp_grid

def all_batteries_capped(house: House, batteries: list[Battery]) -> bool:
    """
    Checks if any battery has enough capacity left
    for a given house.
    Pre: house of class House
         batteries list of objects of class Battery
    Post: returns True if all batteries are at max capacity
          else return False
    """

    for battery in batteries:

        # if a battery has enough capacity, return False
        if battery.is_connection_possible(house) is True:
            return False

    return True

    
def change_grid_hill_climber(tmp_grid, best_cost):
    
    grid = copy.deepcopy(tmp_grid)
    
    house_1 = random.choice(grid.houses)
    
    house_2 = random.choice(grid.houses)
    
    
    while house_1 is house_2:
        house_1 = random.choice(grid.houses)
        house_2 = random.choice(grid.houses)        
        
    battery1 = house_1.connection
    
    battery2 = house_2.connection
    
    # if battery1 is not battery2:
    try:
        if battery1.is_connection_possible(house_2):
            if battery2.is_connection_possible(house_1):
                house_1.delete_connection()
                house_2.delete_connection()
                
                battery1.disconnect_home(house_1)
                battery2.disconnect_home(house_2)
                
                house_1.make_connection(battery2)
                house_2.make_connection(battery1)
                
                battery1.connect_home(house_2)
                battery2.connect_home(house_1)
    except:
        pass
        
        
    cost = grid.calc_cost_shared()
    # if cost != 25000:
    #     print(cost)
    
    if cost < best_cost:
        return [True, cost, grid]
    else:
        return [False, best_cost, grid]