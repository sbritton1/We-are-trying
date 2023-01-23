from ..classes.house import House
from ..classes.grid import Grid

from .possible_swap import possible_swap
import random      
      
def find_random_houses(tmp_grid: Grid) -> list[House, House]:
    """
    Chooses two random houses from all houses in the grid and checks
    if they are not connected to the same battery.
    Pre: grid is of class Grid
    Post: returns two different houses as house object
    """

    while True:
        house1: House = random.choice(tmp_grid.houses)
        house2: House = random.choice(tmp_grid.houses)
        while house2.connection == house1.connection:
            house2: House = random.choice(tmp_grid.houses)

        if possible_swap(house1, house2) is True:
            break

    return house1, house2