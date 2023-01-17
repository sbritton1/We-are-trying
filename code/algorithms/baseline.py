import random
import matplotlib.pyplot as plt
from ..classes.grid import Grid
from ..classes.house import House
from ..classes.battery import Battery
import copy

def baseline(grid: Grid) -> Grid:
    """
    Creates a baseline for what cost we can expect, based on what
    the cost would be if the houses are randomly connected to batteries.
    Pre: grid is of class Grid
    Post: returns lowest cost solution
    """

    # keeps track of costs of all solutions
    costs: list[int] = []
    best_solution: Grid = grid

    # 1000 iterations
    for _ in range(1000):

        # create a temporary grid, all houses are connected to random battery
        tmp_grid: Grid = add_connections(grid)
        cost: int = tmp_grid.calc_cost_normal()

        # add cost to list and check if it's the new best solution
        costs.append(cost)
        if min(costs) == cost:
            best_solution = tmp_grid

    # make histogram of costs of all solutions
    plot_cost(costs)

    return best_solution


def add_connections(grid: Grid) -> Grid:
    """
    Connects houses to random batteries.
    Pre: grid is of class Grid
    Post: returns a copy of original grid, in which
          houses are randomly connected to a battery
    """

    # create deepcopy of original grid
    tmp_grid = copy.deepcopy(grid)

    # ! Hier kunnen we slimmer checken of alle batterijen al zijn gecapped om
    # ! zo minder vaak te checken of alles gecapped is en ook eerder te stoppen

    for house in tmp_grid.houses:

        # loops until available battery is found
        while True:

            # check if any battery has enough capacity left
            if all_batteries_capped(house, tmp_grid.batteries) is True:
                break

            # select random battery
            battery = random.choice(tmp_grid.batteries)

            # if battery has enough capacity left, make connection
            if battery.is_connection_possible(house) is True:
                battery.connect_home(house)
                house.make_connection(battery)
                break

    return tmp_grid


def all_batteries_capped(house: House, batteries: list[Battery]) -> bool:
    """
    Checks if any battery has enough capacity left
    for a given house.
    Pre: house of class House
         batteries list of objects of class Battery
    Post: returns True if all batteries are at max capacity
          else return False
    """

    for battery in batteries:

        # if a battery has enough capacity, return False
        if battery.is_connection_possible(house) is True:
            return False

    return True


def plot_cost(costs: list[int]):
    """
    Plots a histogram of the costs of all solutions.
    Pre: costs is a list of ints
    Post: displays histogram
    """

    plt.hist(costs)
    plt.xlabel("Cost")
    plt.ylabel("quantity")
    plt.show()

