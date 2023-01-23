from ..classes.grid import Grid
from ..classes.house import House
from ..classes.battery import Battery
import random

def resolve_error(grid: Grid) -> None:
    """
    Tries to make an invalid grid a valid solution.
    
    Pre : grid of class Grid
    Post: each house in grid is connected to a battery
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

    # battery with higher weight is more likely to get picked
    best_bat = random.choices(grid.batteries, weights=battery_weights, k=1)[0]

    # check if battery has enough capacity for unconnected house
    if best_bat.is_connection_possible(unconnected) is True:
        best_bat.connect_home(unconnected)
        unconnected.make_connection(best_bat)
        return
    
    # if house does not fit, run this
    while True:

        # give house a weight to get picked
        house_weights: list[float] = []
        for house in best_bat.connected_homes:
            house_weights.append(1/house.maxoutput)

        # select random house based on weight
        house: House = random.choices(best_bat.connected_homes, weights=house_weights, k=1)[0]

        # checks if possible to connect unconnected house if random
        # house gets disconnected
        if house.maxoutput + best_bat.current_capacity > unconnected.maxoutput:

            # disconnect original house
            best_bat.disconnect_home(house)
            house.delete_connection()

            # connect the previous unconnected house
            best_bat.connect_home(unconnected)
            unconnected.make_connection(best_bat)

            # run function again to solve newly unconnected house
            resolve_error(grid)

            return