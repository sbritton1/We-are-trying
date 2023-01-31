from ..classes.grid import Grid
from ..classes.battery import Battery
from ..classes.house import House
from typing import Any
import json


def to_json(grid: Grid, cable_type: str) -> None:
    """
    Exports the data to a json file in the prescribed format.
    
    Pre : grid is of class Grid
    Post: .json file is created
    """

    # list of dictionaries
    all_dicts: list[dict[str, Any]] = []

    # Create dictionary with information about grid itself
    grid_dict: dict[str, Any] = {}
    grid_dict["district"] = grid.district
    
    if cable_type == "unique":
        grid_dict["costs-own"] = grid.cost
    elif cable_type == "shared":
        grid_dict["costs-shared"] = grid.cost
    all_dicts.append(grid_dict)

    add_batteries(grid, all_dicts)

    # Create json file based on the data
    json_object = json.dumps(all_dicts, indent=4)

    # write output.json file
    with open("results/output.json", "w") as outfile:
        outfile.write(json_object)


def add_batteries(grid: Grid, all_dicts: list[dict[str, Any]]) -> None:
    """
    Adds battery information to the full list of dictionaries, that will
    get turned into a json file.

    Pre : grid is of class Grid, all_dicts is a list of dictionaries
    Post: all necessary information for each battery is added 
          to the complete list
    """

    # For each battery, create its own dictionary
    for battery in grid.batteries:
        bat_dict: dict[str, Any] = {}
        bat_dict["location"] = f"{battery.coord_x},{battery.coord_y}"
        bat_dict["capacity"] = battery.total_capacity

        # add the house information to the battery dict
        bat_dict["houses"] = add_houses(battery)

        # add battery dict to full list
        all_dicts.append(bat_dict)


def add_houses(battery: Battery) -> list[dict[str, Any]]:
    """
    Adds house information of a battery to list of dictionaries.

    Pre : battery is of class Battery
    Post: returns list of dicts of string and any, in which the dictionaries
          contains all the information of each individual house
    """

    # list of dictionaries
    houses: list[dict[str, Any]] = []

    #  create dict for each house connected to battery
    for house in battery.connected_homes:
        house_dict: dict[str, Any] = {}
        house_dict["location"] = f"{house.coord_x},{house.coord_y}"
        house_dict["output"] = house.maxoutput
        house_dict["cables"] = house.cables
        houses.append(house_dict)

    return houses
