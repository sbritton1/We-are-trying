from ...classes.grid import Grid
from ...classes.house import House
from ...classes.battery import Battery
from ...helper_functions.valid_solution import valid_solution
from ...helper_functions.resolve_error import resolve_error
import random
import copy


def init_simulated_annealing(grid: Grid) -> Grid:

    # keeps track of costs of all solutions
    lowest_cost: int = None
    best_solution: Grid = None

    for i in range(10):
        print(f"=============================={i}==============================")
        tmp_grid: Grid = copy.deepcopy(grid)
        tmp_grid = add_random_connections(tmp_grid)

        while valid_solution(tmp_grid) is False:
            resolve_error(tmp_grid)
        
        tmp_grid.lay_shared_cables()

        tmp_grid: Grid = simulated_annealing(tmp_grid)

        cost: int = tmp_grid.calc_cost_shared()

        if lowest_cost is None or cost < lowest_cost:
            lowest_cost = cost
            best_solution = tmp_grid

    best_solution.remove_cables()
    return best_solution


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


def simulated_annealing(grid: Grid) -> Grid:
    cost_grid = grid.calc_cost_shared()
    iteration = 0
    last_update = 0

    while iteration < 10000:
        print(iteration)
        tmp_grid = copy.deepcopy(grid)

        while True:
            house1: House = random.choice(tmp_grid.houses)
            house2: House = random.choice(tmp_grid.houses)
            while house2 == house1:
                house2: House = random.choice(tmp_grid.houses)

            if possible_swap(house1, house2) is True:
                break
        
        swap_houses(house1, house2)
        
        tmp_grid.remove_cables()
        tmp_grid.lay_shared_cables()

        new_cost = tmp_grid.calc_cost_shared()
        if new_cost < cost_grid:
            grid = tmp_grid
            cost_grid = new_cost
            last_update = iteration
        else:
            temperature = 1000 * (0.997 ** iteration)
            acceptation_chance = 2 ** ((cost_grid - new_cost) / temperature)
            if acceptation_chance > random.random():
                grid = tmp_grid
                cost_grid = new_cost
                last_update = iteration

        iteration += 1
        if iteration - last_update == 100:
            break

    return grid


def possible_swap(house1: House, house2: House) -> bool:
    if house1.maxoutput > house2.maxoutput + house2.connection.current_capacity:
        return False

    elif house2.maxoutput > house1.maxoutput + house1.connection.current_capacity:
        return False

    return True


def swap_houses(house1: House, house2: House):
    house1_bat: Battery = house1.connection
    house2_bat: Battery = house2.connection

    house1_bat.disconnect_home(house1)
    house1.delete_connection()
    house2_bat.disconnect_home(house2)
    house2.delete_connection()

    house1_bat.connect_home(house2)
    house2.make_connection(house1_bat)
    house2_bat.connect_home(house1)
    house1.make_connection(house2_bat)