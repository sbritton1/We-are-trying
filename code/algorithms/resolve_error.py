from ..classes.grid import Grid
from ..classes.house import House
from ..classes.battery import Battery
import random

def resolve_error(grid: Grid) -> None:
    unconnected: House = None

    for house in grid.houses:
        if house.has_connection is False:
            unconnected = house

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

        if house.maxoutput + best_bat.current_capacity > unconnected.maxoutput:
            best_bat.disconnect_home(house)
            house.delete_connection()

            best_bat.connect_home(unconnected)
            unconnected.make_connection(best_bat)

            resolve_error(grid)

            return