import random

def baseline(grid):
    for house in grid.houses:
        battery = random.choice(grid.batteries)
        battery.connect_home(house)
        house.make_connection(battery)