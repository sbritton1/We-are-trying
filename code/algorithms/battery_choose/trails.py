from copy import copy

from ...classes.grid import Grid
from ...classes.battery import Battery
from ...classes.house import House

batteries = {
    450: {"type": "Powerstar", "cost": 900},
    900: {"type": "Imerse-II", "cost": 1350},
    1800: {"type": "Imerse-III", "cost": 1800},
}

def trails(grid: Grid) -> Grid:

    # make a shallow copy of the houses list
    houses_copy = copy(grid.houses)

    # go over all houses

        # go over all remaining houses in the shallow copy and find the
        # distance, remove this considered house from the shallow copy

    # connect the closest houses

    # repeat untill all houses are connected

    # look if trails can be combined or 
    

    return grid


class Trail():
    def __init__(self) -> None:
        self.houses: list[House] = []
        self.total_load = 0.0

        self.battery = batteries[450]

    def connect_house(self, house: House) -> None:
        self.houses.append(house)
        self.total_load += house.maxoutput

    def get_distance_to_house(self, house: House) -> int:

        min_distance = 999

        house_x, house_y = house.coord_x, house.coord_y
        
        for trail_house in self.houses:
            trail_x, trail_y = trail_house.coord_x, trail_house.coord_y

            abs_dist_x = abs(trail_x - house_x)
            abs_dist_y = abs(trail_y - house_y)

            distance = abs_dist_x + abs_dist_y

            min_distance = min(min_distance, distance)

        return min_distance

        


            