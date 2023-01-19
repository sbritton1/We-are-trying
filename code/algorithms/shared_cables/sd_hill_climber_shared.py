from ...classes.grid import Grid
from ...classes.house import House
from ...classes.battery import Battery
from ...helper_functions.valid_solution import valid_solution
from ...helper_functions.resolve_error import resolve_error
import random
import copy


def init_sd_hill_climber_shared(grid: Grid) -> Grid:

    # keeps track of costs of all solutions
    lowest_cost: int = None
    best_solution: Grid = None

    for i in range(1):
        tmp_grid: Grid = copy.deepcopy(grid)
        tmp_grid = add_random_connections(tmp_grid)

        while valid_solution(tmp_grid) is False:
            resolve_error(tmp_grid)

        sd_hill_climber_shared(tmp_grid)

        cost: int = tmp_grid.calc_cost_normal()

        if lowest_cost is None or cost < lowest_cost:
            lowest_cost = cost
            best_solution = tmp_grid

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


def sd_hill_climber_shared(grid: Grid) -> None:
    grid.lay_shared_cables()
    best_cost = grid.calc_cost_shared()

    while True:
        best_improvement: int = 0
        target1: House = None
        target2: House = None

        for house1 in grid.houses:
            print("check")
            for house2 in grid.houses:
                if house1.connection != house2.connection:
                    if possible_swap(house1, house2) is True:
                        improvement = calc_improvement(grid, best_cost, house1, house2)
                        if improvement > best_improvement:
                            best_improvement = improvement
                            target1 = house1
                            target2 = house2

        if best_improvement == 0:
            return

        else:
            swap_houses(target1, target2)
            grid.remove_cables()
            grid.lay_shared_cables()
            best_cost = grid.calc_cost_shared()


def possible_swap(house1: House, house2: House) -> bool:
    if house1.maxoutput > house2.maxoutput + house2.connection.current_capacity:
        return False

    elif house2.maxoutput > house1.maxoutput + house1.connection.current_capacity:
        return False

    return True


def calc_improvement(grid: Grid, org_cost: int, house1: House, house2: House) -> int:
    grid.remove_cables()
    swap_houses(house1, house2)
    grid.lay_shared_cables()
    new_cost = grid.calc_cost_shared()
    grid.remove_cables()
    swap_houses(house1, house2)

    return org_cost - new_cost


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