from ..classes.grid import Grid
from ..classes.house import House
from ..classes.battery import Battery
import random
import copy


def init_steepest_descent_hill_climber(grid: Grid) -> Grid:

    # keeps track of costs of all solutions
    lowest_cost: int = None
    best_solution: Grid = None

    for i in range(1000):
        tmp_grid: Grid = copy.deepcopy(grid)
        tmp_grid = add_random_connections(tmp_grid)
        steepest_descent_hill_climber(tmp_grid)

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


def steepest_descent_hill_climber(grid: Grid) -> None:
    improve_loc: int = 0

    while True:
        grid.houses.sort(key=lambda house: house.distance_to_battery(), reverse=True)

        best_improvement: int = 0
        target: House = None

        for house in grid.houses[improve_loc:]:
            if possible_swap(grid.houses[improve_loc], house) is True:
                improvement = calc_improvement(grid.houses[improve_loc], house)
                if improvement > best_improvement:
                    best_improvement = improvement
                    target = house

        if best_improvement == 0:
            improve_loc += 1
            if improve_loc == len(grid.houses):
                return

        else:
            swap_houses(grid.houses[improve_loc], target)


def possible_swap(house1: House, house2: House) -> bool:
    if house1.maxoutput > house2.maxoutput + house2.connection.current_capacity:
        return False

    elif house2.maxoutput > house1.maxoutput + house1.connection.current_capacity:
        return False

    return True


def calc_improvement(house1: House, house2: House) -> int:
    diff1 = house1.distance_to_battery() - house1.distance_to_any_battery(house2.connection)
    diff2 = house2.distance_to_battery() - house2.distance_to_any_battery(house1.connection)

    return diff1 + diff2


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
