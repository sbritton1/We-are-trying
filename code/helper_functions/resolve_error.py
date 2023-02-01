import random

from ..classes.grid import Grid
from ..classes.house import House
from ..classes.battery import Battery


def resolve_error(grid: Grid) -> None:
    """
    Tries to make an invalid grid a valid solution.

    Pre : grid of class Grid
    Post: each house in grid is connected to a battery

    Side-effects: A very small chance this function gets stuck
                  and the resulting grid is still not valid.

                  Function assumes only a single house is not connected,
                  run multiple times when this is not the case.
    """

    unconnected: House = None

    # save unconnected house
    for house in grid.houses:
        if house.has_connection is False:
            unconnected = house

    # use current capacity of batteries as weights to sort by
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
    else:
        swap_unconnected(grid, unconnected, best_bat)
        return


def swap_unconnected(grid: Grid, unconnected_house: House,
                     battery: Battery) -> None:
    """
    Swaps unconnected house with a house connected to the battery,
    with a high chance that this house has a lower max output than
    the unconnected house, to hopefully be able to freely connect
    that house to another battery. Then calls resolve_error() to connect
    newly unconnected house to a battery.

    Pre : grid is of class Grid, unconnected_house is of class House,
          battery is of class Battery
    Post: unconnected house is now connected to a battery, and resolve_error()
          will be run to fix the newly unconnected house
    """

    # allow for 10000 swaps to attempt to resolve the error
    max_swap_attempts = 10000
    for _ in range(max_swap_attempts):

        # give house a weight to get picked
        house_weights: list[float] = []
        for house in battery.connected_homes:
            house_weights.append(1/house.maxoutput)

        # select random house based on weight
        house: House = random.choices(battery.connected_homes,
                                      weights=house_weights, k=1)[0]

        # checks if possible to connect unconnected house if random
        # house gets disconnected
        available_capacity = house.maxoutput + battery.current_capacity
        if available_capacity > unconnected_house.maxoutput:

            # disconnect original house
            battery.disconnect_home(house)
            house.delete_connection()

            # connect the previous unconnected house
            battery.connect_home(unconnected_house)
            unconnected_house.make_connection(battery)

            # run function again to solve newly unconnected house
            resolve_error(grid)

            return
