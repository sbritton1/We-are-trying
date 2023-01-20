from ..classes.grid import Grid
from ..classes.house import House
from ..classes.battery import Battery
import random

def resolve_error(grid: Grid) -> None:
    """
    Tries to make an invalid grid a valid solution.
    
    Pre: grid of class Grid
    Post: none
    """
    unconnected: House = None

    # saves unconnected house
    for house in grid.houses:
        if house.has_connection is False:
            unconnected = house

    # saves all the current capacities of the batteries
    battery_weights = []
    for battery in grid.batteries:
        battery_weights.append(battery.current_capacity)

    best_bat = random.choices(grid.batteries, weights=battery_weights, k=1)[0]

    if best_bat.is_connection_possible(unconnected) is True:
        best_bat.connect_home(unconnected)
        unconnected.make_connection(best_bat)
        return

    for i in range(10000):
        house_weights = []
        for house in best_bat.connected_homes:
            house_weights.append(1/house.maxoutput)

        house = random.choices(best_bat.connected_homes, weights=house_weights, k=1)[0]

        # ! handig om te checken of de comment wel klopt
        # checks if it is possible to connect unconnected house if random
        # house gets disconnected
        if house.maxoutput + best_bat.current_capacity > unconnected.maxoutput:
            best_bat.disconnect_home(house)
            house.delete_connection()

            best_bat.connect_home(unconnected)
            unconnected.make_connection(best_bat)

            resolve_error(grid)

            return