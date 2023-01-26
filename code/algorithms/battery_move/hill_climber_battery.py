from ...classes.grid import Grid
from ...classes.battery import Battery
from ..shared_cables.hill_climber_shared import init_hill_climber_shared
from ..own_cables.greedy import greedy
import copy
import multiprocessing
import random


def init_hill_climber_battery(grid: Grid) -> Grid:

    # create list of grids as work for multithreading
    grids: list[Grid] = []

    # amount of grids to run algorithm on
    for _ in range(6):

        # create deepcopy to not mess with original
        tmp_grid = copy.deepcopy(grid)
        randomize_battery_placement(tmp_grid)
        tmp_grid = greedy(tmp_grid)

        tmp_grid.lay_shared_cables()
        tmp_grid.calc_cost_shared()

        grids.append(tmp_grid)

    # use multithread processing, with workers amount of threads
    workers: int = 6
    p = multiprocessing.Pool(workers)
    results = (p.map(hill_climber_battery, grids))

    best_result: Grid = None
    best_costs: list[int] = [1000000]
    for result in results:
        new_grid = result[0]
        costs = result[1]
        if costs[-1] < best_costs[-1]:
            best_costs = costs
            best_result = new_grid

    print(f"Best cost: {best_result.cost}")
    best_result = init_hill_climber_shared(best_result, False)

    return best_result


def randomize_battery_placement(grid: Grid) -> None:
    for battery in grid.batteries:
        new_x = -1
        new_y = -1 
        
        while grid.move_battery(battery, new_x, new_y) is False:
            new_x = random.choice(list(range(grid.size_grid()[0])))
            new_y = random.choice(list(range(grid.size_grid()[1])))
        


def hill_climber_battery(grid: Grid) -> tuple[Grid, list[int]]:
    org_cost: int = grid.cost
    costs: list[int] = []
    last_improvement: int = 0
    iteration: int = 0

    while iteration - last_improvement < 100 and iteration < 1000:
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
    battery: Battery = random.choice(grid.batteries)

    target_x: int = battery.coord_x
    target_y: int = battery.coord_y
    
    while grid.move_battery(battery, target_x, target_y) is False:
        target_x += random.choice(list(range(-10, 10, 1)))
        target_x = track_size(grid, target_x, 0)

        target_y += random.choice(list(range(-10, 10, 1)))
        target_y = track_size(grid, target_y, 1)


def track_size(grid: Grid, coord: int, dir: int) -> int:
    if coord < 0:
        coord = 0
    elif coord > grid.size_grid()[dir]:
        coord = grid.size_grid()[dir]

    return coord
