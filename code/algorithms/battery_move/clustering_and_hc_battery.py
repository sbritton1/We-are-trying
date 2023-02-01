from .clustering import clustering
from .hill_climber_battery import init_hill_climber_battery
from ...classes.grid import Grid


def clustering_and_hc_battery(grid: Grid) -> Grid:
    """
    Uses the clustering algorithm to create startpoints for the hill climber
        battery algorithm.

    Pre : grid is a Grid object without any connections and batteries already
        placed
    Post: the best solution of hill climber battery is returned, with the grid
        having its connections
    """

    # get a grid without connections, but clustered batteries
    grid = clustering(grid, connect=False)

    # let the hill climber battery do its thing, without using randomised start
    # points
    grid = init_hill_climber_battery(grid, randomize=False)

    return grid
