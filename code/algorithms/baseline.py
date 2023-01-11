import random
import matplotlib.pyplot as plt
import copy

def baseline(grid):

    costs: list[int] = []

    for i in range(1000):
        tmp_grid = add_connections(grid)
        cost = price(tmp_grid)
        costs.append(cost)
        
    plot_cost(costs)


def add_connections(grid):
    tmp_grid = copy.deepcopy(grid)

    for house in tmp_grid.houses:
        battery = random.choice(tmp_grid.batteries)
        battery.connect_home(house)
        house.make_connection(battery)

    return tmp_grid

def price(tmp_grid):
    cost: int = 0
    cost += len(tmp_grid.batteries) * 5000
    print(cost)

    for house in tmp_grid.houses:
        cost += house.distance_to_battery * 9
    
    print(f"Total cost = {cost}")

    return cost

def plot_cost(costs: list[int]):
    plt.hist(costs)

