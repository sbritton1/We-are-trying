from ..classes.grid import Grid


def valid_solution(grid: Grid) -> bool:
    """
    Checks if valid solution to grid has been found by
    seeing if every house has a connection to a battery.

    Pre : grid is of class Grid
    Post: returns True if solution is valid
          returns False if solution is invalid
    """

    for house in grid.houses:
        if house.has_connection is False:
            return False

    return True
