import json
from ..classes.grid import Grid
from ..classes.house import House
from ..classes.battery import Battery

def convert_from_JSON(filepath: str) -> Grid:
    f = open(filepath)
  
    # returns JSON object as a dictionary
    data = json.load(f)
    
    # get the grid info
    grid_info = data[0]

    # create the grid and set cost
    grid = Grid(grid_info['district'], load_csv=False)
    grid.set_cost(grid_info['costs-shared'])

    batteries_and_houses_info = data[1:]

    for battery_and_houses_info in batteries_and_houses_info:
        load_battery_and_houses(grid, battery_and_houses_info)

    return grid


def load_battery_and_houses(grid: Grid, battery_and_houses_info: dict) -> None:
    # get battery info and create a battery object
    battery = load_battery(battery_and_houses_info)

    # get houses info and loop over it
    houses_info = battery_and_houses_info['houses']
    for house_info in houses_info:
        house = load_house(house_info, battery)

        battery.connect_home(house)
        grid.add_house(house)

    grid.add_battery(battery)


def load_battery(battery_info) -> Battery:
    # read battery information
    x, y, capacity = read_battery_info(battery_info)

    # make battery object
    return Battery(x, y, capacity)


def read_battery_info(battery_info: dict) -> tuple[int, int, float]:
    # read dictionary
    coordinates, capacity = battery_info['location'], battery_info['capacity']
    
    return convert_data(coordinates, capacity)


def read_house_info(house_info: dict) -> tuple[int, int, float]:
    # read dictionary
    coordinates, output = house_info['location'], house_info['output']
    
    return convert_data(coordinates, output)


def convert_data(coordinates: str, property: str) -> tuple[int, int, float]:
    # convert data
    x, y = [int(coordinate) for coordinate in coordinates.split(',')]
    property = float(property)

    return (x, y, property)


def load_house(house_info: dict, battery: Battery) -> House:
    # read house information
    x, y, output = read_house_info(house_info)

    house = House(x, y, output)

    house.make_connection(battery)
    house.set_cables(house_info['cables'])

    return house
