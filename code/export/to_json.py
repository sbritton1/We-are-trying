from ..classes.grid import Grid
from typing import Any
import json

def to_json(grid: Grid) -> None:
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
    grid_dict["costs-shared"] = grid.cost
    all_dicts.append(grid_dict)

    # For each battery, create its own dictionary
    for battery in grid.batteries:
        bat_dict: dict[str, Any] = {}
        bat_dict["location"] = f"{battery.coord_x},{battery.coord_y}"
        bat_dict["capacity"] = battery.total_capacity

        # list of dictionaries
        houses: list[dict[str, Any]] = []

        #  create dict for each house connected to battery
        for house in battery.connected_homes:
            house_dict = {}
            house_dict["location"] = f"{house.coord_x},{house.coord_y}"
            house_dict["output"] = house.maxoutput
            house_dict["cables"] = house.cables
            houses.append(house_dict)

        # add the house information to the battery dict
        bat_dict["houses"] = houses

        # add battery dict to full list
        all_dicts.append(bat_dict)

    # Create json file based on the data
    json_object = json.dumps(all_dicts, indent=4)

    # write output.json file
    with open("results/output.json", "w") as outfile:
        outfile.write(json_object)
