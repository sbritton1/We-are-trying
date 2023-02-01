import random

from ..classes.house import House
from ..classes.grid import Grid
from .possible_swap import possible_swap


def find_random_houses(grid: Grid) -> tuple[House, House]:
    """
    Chooses two random houses from all houses in the grid and checks
    if they are not connected to the same battery.

    Pre : grid is of class Grid
    Post: returns two different houses as house object
    """

    # pick random houses until a swap is possible
    while True:
        house1: House = random.choice(grid.houses)
        house2: House = random.choice(grid.houses)

        # swap is possible if both houses are not connected to the same
        # battery and both batteries have enough capacity
        if possible_swap(house1, house2) is True:
            break

    return house1, house2
