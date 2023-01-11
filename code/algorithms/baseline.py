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
        while True:
            if all_batteries_capped(house, tmp_grid.batteries) is True:
                break

            battery = random.choice(tmp_grid.batteries)

            if battery.is_connection_possible(house) is True:
                battery.connect_home(house)
                house.make_connection(battery)
                break

    return tmp_grid

def all_batteries_capped(house, batteries):
    state = True

    for battery in batteries:
        if battery.is_connection_possible(house) is True:
            state = False
            break

    return state


def price(tmp_grid):
    cost: int = 0
    cost += len(tmp_grid.batteries) * 5000

    qty_unconnected_houses = 0

    for house in tmp_grid.houses:
        if house.has_connection == True:
            cost += house.distance_to_battery() * 9
        else:
            qty_unconnected_houses += 1

    return cost


def plot_cost(costs: list[int]):
    plt.hist(costs)
    plt.show()

