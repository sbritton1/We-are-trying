from .clustering import clustering
from .hill_climber_battery import init_hill_climber_battery
from ...classes.grid import Grid


def clustering_and_hill_climber_battery(grid: Grid) -> Grid:
    grid = clustering(grid)

    grid.remove_all_connections()

    grid = init_hill_climber_battery(grid, randomize=False)

    return grid
