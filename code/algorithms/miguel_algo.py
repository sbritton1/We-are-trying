from ..classes.grid import Grid
from ..classes.house import House
from ..classes.battery import Battery

def miguel_algo(grid: Grid) -> Grid:
    unconnected: list[int] = [*range(len(grid.houses))]

    for i in range(len(grid.houses)):
        minimum = find_minimum(grid, unconnected)
        if minimum == (None, None):
            break

        battery = minimum[0]
        house = grid.houses[minimum[1]]
        unconnected.remove(minimum[1])

        house.make_connection(battery)
        battery.connect_home(house)

    cost = price(grid)
    grid.add_cost(cost)

    return grid


def find_minimum(grid: Grid, unconnected: list[int]) -> tuple[Battery, int]:
    min_distance = 100
    minimum = (None, None)

    for battery in grid.batteries:
        for i in unconnected:
            distance = grid.houses[i].distance_to_any_battery(battery)
            possible_connection = battery.is_connection_possible(grid.houses[i])
            if distance < min_distance and possible_connection:
                min_distance = distance
                minimum = (battery, i)

    return minimum

def price(grid: Grid) -> int:
    """
    Calculates the price of a grid.
    Pre: tmp_grid is of class Grid
    Post: returns an int cost
    """

    cost: int = 0

    # each battery in the grid costs 5000
    cost += len(grid.batteries) * 5000

    # not every house may be connected to a battery
    qty_unconnected_houses = 0

    for house in grid.houses:
        if house.has_connection == True:

            # each grid piece length of cable costs 9
            cost += house.distance_to_battery() * 9
        else:
            qty_unconnected_houses += 1

    return cost

