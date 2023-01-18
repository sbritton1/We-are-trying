from ...classes.grid import Grid
from ...classes.house import House
from ...classes.battery import Battery
from ...helper_functions.valid_solution import valid_solution
from ...helper_functions.resolve_error import resolve_error
import random
import copy


def testen_algo(grid: Grid):
    # maak random grid
    # tmp_grid = add_connections(grid)
    
    # tmp_grid: Grid = copy.deepcopy(grid)
    tmp_grid = add_random_connections(grid)

    while valid_solution(tmp_grid) is False:
        resolve_error(tmp_grid)
    
    # maak best cost die altijd verbeterd kan worden 
    best_cost = 10000000
    
    my_condition = 0
    
    always = 0

    # loop die stopt wanneer 500 keer geen verbetering te zien is
    while my_condition < 300 and always < 5000:
        print(always) 
        
        # verandert de grid op een aantal willekeurige plekken
        new_try = change_grid_hill_climber(tmp_grid, best_cost)
        
        # conditie om te kijken of het een betere oplossing
        if new_try[0]:
            my_condition = 0
            best_cost = new_try[1]
            tmp_grid = new_try[2]
        else:
            my_condition += 1
        always += 1
        print("\n")
        print(best_cost)
            
    return tmp_grid
    
def add_random_connections(tmp_grid: Grid) -> Grid:
    """
    Connects houses to random batteries.
    Pre: grid is of class Grid
    Post: returns a copy of original grid, in which
          houses are randomly connected to a battery
    """

    for house in tmp_grid.houses:

        # loops until available battery is found
        for i in range(len(tmp_grid.batteries)):
            random.shuffle(tmp_grid.batteries)

            # select random battery
            battery: Battery = tmp_grid.batteries[i]

            # if battery has enough capacity left, make connection
            if battery.is_connection_possible(house) is True:
                battery.connect_home(house)
                house.make_connection(battery)
                break

    return tmp_grid

    
def change_grid_hill_climber(tmp_grid, best_cost):
    # 200x random veranderingen proberen te doen
    for _ in range(20):
        grid = copy.deepcopy(tmp_grid)
        
        house_1 = random.choice(grid.houses)
        
        house_2 = random.choice(grid.houses)
        
        
        while house_1 is house_2 and house_1.connection is house_2.connection:
            house_1 = random.choice(grid.houses)
            house_2 = random.choice(grid.houses)        
            
        battery1 = house_1.connection
        
        battery2 = house_2.connection
        
        try:
            house_1.delete_connection()
            house_2.delete_connection()
            
            battery1.disconnect_home(house_1)
            battery2.disconnect_home(house_2)
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
        except:
            pass
    
    
    # maakt een kopie, zodat er kosten kunnen worden berekend op basis van
    # de shared cables
    test_grid = copy.deepcopy(grid)
    
    # legt kabels in de kopie grid
    for battery in test_grid.batteries:
        battery.lay_shared_cables()
        
    # kosten voor kopie grid 
    cost = test_grid.calc_cost_shared()
    
    if cost < best_cost and valid_solution(grid):
        return [True, cost, grid]
    else:
        return [False, best_cost, grid]
