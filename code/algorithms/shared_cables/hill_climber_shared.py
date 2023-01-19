from ...classes.grid import Grid
from ...classes.house import House
from ...classes.battery import Battery
from ...helper_functions.valid_solution import valid_solution
from ...helper_functions.resolve_error import resolve_error
import random
import copy


def testen_algo(grid: Grid):
    """
    dit is een hill climber algoritme
    """
    # maak random grid aan
    tmp_grid = add_random_connections(grid)

    # zorg dat random grid een 
    while valid_solution(tmp_grid) is False:
        resolve_error(tmp_grid)
    
    # maak best cost die altijd verbeterd kan worden 
    best_cost = 10000000
    
    # initaliseren condities
    times_no_improvement = 0
    max_iterations = 0

    # loop die stopt wanneer 300 keer geen verbetering te zien is
    while times_no_improvement < 300 and max_iterations < 5000:
        print(max_iterations) 
        
        # verandert de grid op een aantal willekeurige plekken
        changed_grid_and_costs = change_grid_hill_climber(tmp_grid, best_cost)
        
        # conditie om te kijken of het een betere oplossing
        if changed_grid_and_costs[0]:
            times_no_improvement = 0
            best_cost = changed_grid_and_costs[1]
            tmp_grid = changed_grid_and_costs[2]
        else:
            times_no_improvement += 1


        max_iterations += 1
        
        # print functies om te testen
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

    
def change_grid_hill_climber(tmp_grid, best_cost) -> list[bool, int, Grid]:
    """
    Deze functie probeert een n aantal keer huizen anders te verbinden aan
    een batterij om zo tot een verbetering te komen van de grid.
    """
    # 20x random veranderingen proberen te doen
    for _ in range(20):
        grid = copy.deepcopy(tmp_grid)
        
        house_1, house_2 = find_random_houses(grid)    
            
        battery1 = house_1.connection
        
        battery2 = house_2.connection
        
        swap_houses(house_1, house_2, battery1, battery2)   
    
    # maakt een kopie, zodat er kosten kunnen worden berekend op basis van
    # de shared cables
    test_grid = copy.deepcopy(grid)
    
    # legt kabels in de kopie grid
    for battery in test_grid.batteries:
        battery.lay_shared_cables()
        
    # kosten voor kopie grid 
    cost = test_grid.calc_cost_shared()
    
    # checkt verbetering
    new_cost = check_if_improvement(cost, best_cost, grid)
    
    return new_cost
    
    
def find_random_houses(grid: Grid) -> list[House, House]:
    """
    deze functie vindt random huizen die niet aan dezelfde batterij verbonden zijn 
    """
    house_1 = random.choice(grid.houses)
    house_2 = random.choice(grid.houses)
        
    # kiest nieuwe huizen als ze aan dezelfde batterij verbonden zijn
    while house_1 is house_2 and house_1.connection is house_2.connection:
        house_1 = random.choice(grid.houses)
        house_2 = random.choice(grid.houses) 
        
    return house_1, house_2   


def check_if_improvement(cost: int, best_cost: int, grid: Grid) -> list[bool, int, Grid]:
    """
    checkt of de nieuwe grid met nieuwe plekken voor de huizen een betere oplossing is
    """
    # checkt of de kosten verlaagd zijn, en of het nog een goede oplossing is
    if cost <= best_cost and valid_solution(grid):
        return [True, cost, grid]
    else:
        return [False, best_cost, grid]
    
# mogelijke verbetering: pas deleten wanneer connectie mogelijk
def swap_houses(house_1: House, house_2: House, battery1: Battery, battery2: Battery) -> None:
    """
    swapt 2 huizen wanneer er geen probleem ontstaat voor de capaciteit van het probleem    
    """
    # verwijderen connectie huizen met batterijen
    house_1.delete_connection()
    house_2.delete_connection()
    
    battery1.disconnect_home(house_1)
    battery2.disconnect_home(house_2)
    
    # swapt huizen als capaciteit dat toestaat, anders weer naar default positie
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
