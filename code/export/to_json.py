import json

def to_json(grid):
    all_dicts = []

    grid_dict = {}
    grid_dict["district"] = grid.district
    grid_dict["costs-shared"] = grid.cost
    all_dicts.append(grid_dict)

    for battery in grid.batteries:
        bat_dict = {}
        bat_dict["location"] = f"{battery.coord_x, battery.coord_y}"
        bat_dict["capacity"] = f"{battery.total_capacity}"

        houses = []

        for house in grid.houses:
            house_dict = {}
            house_dict["location"] = f"{house.coord_x, house.coord_y}"
            house_dict["output"] = f"{house.maxoutput}"
            house_dict["cables"] = f"{house.cables}"
            houses.append(house_dict)

        bat_dict["houses"] = houses

        all_dicts.append(bat_dict)

    json_object = json.dumps(all_dicts, indent=4)

    with open("sample.json", "w") as outfile:
        outfile.write(json_object)