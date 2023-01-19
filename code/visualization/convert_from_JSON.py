import json

from ..classes.grid import Grid
from ..classes.house import House
from ..classes.battery import Battery


def convert_from_JSON(filepath: str) -> Grid:
    """
    Loads a Smart Grid from a JSON file
    """

    # load the data from the JSON file as a dictionary
    data = load_data(filepath)

    # get the grid info
    grid_info = data[0]

    # create the grid and set cost
    grid = Grid(grid_info['district'], load_csv=False)
    grid.set_cost(grid_info['costs-shared'])

    # extract the batteries and houses info
    batteries_and_houses_info = data[1:]

    # loop over each battery and its connected houses info and load them into
    # the grid
    for battery_and_houses_info in batteries_and_houses_info:
        load_battery_and_houses(grid, battery_and_houses_info)

    return grid


def load_data(filepath: str) -> dict:
    """
    Loads a JSON file and returns it using the json module
    """

    # open the file
    f = open(filepath)

    # returns JSON object as a dictionary
    return json.load(f)


def load_battery_and_houses(grid: Grid, battery_and_houses_info: dict) -> None:
    """
    Loads the battery and its connected houses as its corresponding objects
    with the loaded cables and connections and add it to the grid
    """

    # get battery info and create a battery object
    battery = load_battery(battery_and_houses_info)

    # get houses info and loop over it
    houses_info = battery_and_houses_info['houses']
    for house_info in houses_info:
        # load house and make house object
        house = load_house(house_info, battery)

        # connect it to the battery
        battery.connect_home(house)

        # add the house to the grid
        grid.add_house(house)

    # add the battery to the grid
    grid.add_battery(battery)


def load_battery(battery_info) -> Battery:
    """
    Load the properties of the battery and return a Battery object with these
    properties
    """

    # read battery information
    x, y, capacity = read_battery_info(battery_info)

    # make battery object
    return Battery(x, y, capacity)


def read_battery_info(battery_info: dict) -> tuple[int, int, float]:
    """
    Reads the battery info stored in the given dictionary and returns it as a
    tuple with the correct data types
    """

    # read dictionary
    coordinates, capacity = battery_info['location'], battery_info['capacity']

    # return the converted data
    return convert_data(coordinates, capacity)


def read_house_info(house_info: dict) -> tuple[int, int, float]:
    """
    Reads the battery info stored in the given dictionary and returns it as a
    tuple with the correct data types
    """

    # read dictionary
    coordinates, output = house_info['location'], house_info['output']

    # return the converted data
    return convert_data(coordinates, output)


def convert_data(coordinates: str, property: str) -> tuple[int, int, float]:
    """
    Converts the data the proper data types and returns it in a tuple
    """

    # split and convert the doordinates
    x, y = [int(coordinate) for coordinate in coordinates.split(',')]

    # convert the property
    property = float(property)

    return (x, y, property)


def load_house(house_info: dict, battery: Battery) -> House:
    """
    Load the properties of the house and return a properly set up House object
    with these properties
    """

    # read house information
    x, y, output = read_house_info(house_info)

    # create house object
    house = House(x, y, output)

    # make the connection with the battery
    house.make_connection(battery)

    # set the cables
    house.set_cables(house_info['cables'])

    return house
