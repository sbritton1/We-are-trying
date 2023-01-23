from ..classes.grid import Grid
from ..classes.house import House
from ..classes.battery import Battery
import random

def add_random_connections(tmp_grid: Grid) -> Grid:
    """
    Connects houses randomly to the batteries.
    
    Pre : grid is of class Grid
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