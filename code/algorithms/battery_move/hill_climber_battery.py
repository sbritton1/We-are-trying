import copy
import multiprocessing
import random

from ...classes.grid import Grid
from ...classes.battery import Battery
from ..shared_cables.hill_climber_shared import init_hill_climber_shared
from ..own_cables.greedy import greedy


def init_hill_climber_battery(grid: Grid, randomize: bool = True) -> Grid:
    """
    Initializes grids with random battery placements and greedy solutions.
    Then calls function to move batteries to try and find a cheaper solution.

    Pre : grid is of class Grid
    Post: returns grid with best found placement of batteries
    """

    # amount of random grids to run hill climber on
    grids_amount = 50

    # create list of grids as work for multithreading
    grids: list[Grid] = create_work(grid, randomize, grids_amount)

    # use multithread processing, with workers amount of threads
    workers: int = 8
    p = multiprocessing.Pool(workers)
    results = (p.map(hill_climber_battery, grids))

    best_result: Grid = analyze_results(results)

    print(f"Best cost: {best_result.cost}")

    # improve connections between houses and batteries using hill climber
    best_result = init_hill_climber_shared(best_result, False)

    return best_result


def create_work(grid: Grid, randomize: bool, amount: int) -> list[Grid]:
    """
    Creates list of work for the workers to go through, by randomizing
    battery placement if wanted. Runs greedy algorithm to get a baseline value
    for the hill climber to improve upon.

    Pre : grid is of class Grid, randomize is a bool, amount is an int
    Post: returns list of Grids, with randomized battery placement if wanted
    """

    grids: list[Grid] = []

    for _ in range(amount):

        # create deepcopy to not mess with original
        tmp_grid = copy.deepcopy(grid)

        if randomize is True:
            randomize_battery_placement(tmp_grid)

        tmp_grid = greedy(tmp_grid)

        tmp_grid.lay_shared_cables()
        tmp_grid.calc_cost_shared()

        grids.append(tmp_grid)

    return grids


def randomize_battery_placement(grid: Grid) -> None:
    """
    Places batteries in random locations in the grid.

    Pre : grid is of class Grid
    Post: batteries have been placed on random coordinates in grid
    """

    for battery in grid.batteries:

        # choose two temporary coords outside of grid
        new_x = -1
        new_y = -1

        # grid.move_battery() returns false when move cannot be made, try again
        while grid.move_battery(battery, new_x, new_y) is False:
            new_x = random.choice(list(range(grid.size_grid()[0])))
            new_y = random.choice(list(range(grid.size_grid()[1])))


def hill_climber_battery(grid: Grid) -> tuple[Grid, list[int]]:
    """
    Runs a hill climber for the battery, gradually moving a battery
    and checking if this results in a cheaper grid.

    Pre : grid is of class Grid
    Post: returns tuple of grid of cheapest found battery configuration and its
          associated cost
    """

    costs: list[int] = [grid.cost]
    last_improvement: int = 0
    iteration: int = 0

    # allow for 100 iterations in which no improvements have been made
    while iteration - last_improvement < 100 and iteration < 1000:

        # make copy of grid, move a random battery and lay the cables for it
        tmp_grid: Grid = copy.deepcopy(grid)
        move_battery(tmp_grid)
        tmp_grid.remove_all_connections()
        tmp_grid = greedy(tmp_grid)
        tmp_grid.lay_shared_cables()
        new_cost = tmp_grid.calc_cost_shared()

        # replace grid if change creates cheaper solution
        if new_cost < grid.cost:
            grid = tmp_grid
            costs.append(new_cost)
            last_improvement = iteration

        iteration += 1

    print(grid.cost)
    return grid, costs


def move_battery(grid: Grid) -> None:
    """
    Moves one random battery to a new location somewhere
    around its current location.

    Pre : grid is of class Grid
    Post: one battery moved a between 0 and 10 steps in each direction
    """

    battery: Battery = random.choice(grid.batteries)

    target_x: int = battery.coord_x
    target_y: int = battery.coord_y

    # grid.move_battery() returns false when chosen location is occupied
    while grid.move_battery(battery, target_x, target_y) is False:

        # move battery random steps in both x and y directions
        target_x = random.choice(list(range(-10, 10, 1)))
        target_x = track_size(grid, target_x, 0)

        target_y = random.choice(list(range(-10, 10, 1)))
        target_y = track_size(grid, target_y, 1)


def track_size(grid: Grid, coord: int, dir: int) -> int:
    """
    Checks if new coordinate is within the grid. If not, place
    coordinate on edge of the board.

    Pre : grid is of class Grid, coord and dir are integers
          dir = 0 means movement in x direction, dir = 1 means y direction
    Post: returns resulting coordinate as integer
    """

    # change coord if it is currently outside of grid size
    if coord < 0:
        coord = 0
    elif coord > grid.size_grid()[dir]:
        coord = grid.size_grid()[dir]

    return coord


def analyze_results(results: list[tuple[Grid, list[int]]]) -> Grid:
    """
    Looks through all the results to find the best solution

    Pre : results is a list of tuples of Grid and a list of ints,
          where the ints is the cost history of the grid
    Post: returns Grid of cheapest solution
    """

    # store cheapest found grid
    best_result: Grid = None

    # arbitrarily large number, so any cost will be below it
    best_costs: list[int] = [1000000]

    # look through results to find cheapest solution
    for result in results:
        new_grid = result[0]
        costs = result[1]
        if costs[-1] < best_costs[-1]:
            best_costs = costs
            best_result = new_grid

    return best_result
