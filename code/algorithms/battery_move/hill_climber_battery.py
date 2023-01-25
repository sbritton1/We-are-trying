from ...classes.grid import Grid
from ...classes.house import House
from ...classes.battery import Battery
from ...helper_functions.valid_solution import valid_solution
from ...helper_functions.resolve_error import resolve_error
from ...helper_functions.add_random_connections import add_random_connections
from ...helper_functions.swap_houses import swap_houses
from ...helper_functions.possible_swap import possible_swap
from ...helper_functions.find_random_houses import find_random_houses
from ..shared_cables.hill_climber_shared import init_hill_climber_shared
from ..own_cables.greedy import greedy
import copy
import multiprocessing
import random


def init_hill_climber_battery(grid: Grid) -> Grid:

    # create list of grids as work for multithreading
    grids: list[Grid] = []

    # amount of grids to run algorithm on
    for _ in range(4):

        # create deepcopy to not mess with original
        tmp_grid = copy.deepcopy(grid)
        tmp_grid = greedy(tmp_grid)

        tmp_grid.lay_shared_cables()
        tmp_grid.calc_cost_shared()

        grids.append(tmp_grid)

    # use multithread processing, with workers amount of threads
    workers = 4
    p = multiprocessing.Pool(workers)
    results = (p.map(hill_climber_battery, grids))

    best_result: Grid = None
    best_costs: list[int] = [1000000]
    for result in results:
        new_grid = result[0]
        costs = result[1]
        print(costs[-1], best_costs[-1])
        if costs[-1] < best_costs[-1]:
            best_costs = costs
            best_result = new_grid

    print(f"Best cost: {best_costs[-1]}")
    best_result = init_hill_climber_shared(best_result)

    return best_result


def hill_climber_battery(grid: Grid) -> tuple[Grid, list[int]]:
    org_cost: int = grid.cost
    costs: list[int] = []
    last_improvement: int = 0
    iteration: int = 0

    while iteration - last_improvement < 50 and iteration < 1000:
        print(iteration)
        tmp_grid: Grid = copy.deepcopy(grid)
        move_battery(tmp_grid)
        tmp_grid.remove_all_connections()
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

    return grid, costs


def move_battery(grid: Grid) -> None:
    battery = random.choice(grid.batteries)

    target_x = battery.coord_x
    target_y = battery.coord_y
    
    while grid.move_battery(battery, target_x, target_y) is False:
        pick_direction = random.choice(["x", "y"])
        if pick_direction == "x":
            target_x +- random.choice([-1, 1])
            target_x = track_size(grid, target_x, 0)
        elif pick_direction == "y":
            target_y += random.choice([-1, 1])
            target_y = track_size(grid, target_y, 1)


def track_size(grid: Grid, coord: int, dir: int) -> int:
    if coord < 0:
        coord += 2
    elif coord > grid.size_grid()[dir]:
        coord -= 2

    return coord
