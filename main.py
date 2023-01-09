import numpy as np
import sys

loc_type = list[tuple[int, int, float]]


def main(district: str):
    file_batteries: str = "data/district_" + district + "/district-" + district + "_batteries.csv"
    file_houses: str= "data/district_" + district + "/district-" + district + "_houses.csv"

    batteries_locs: loc_type = open_file(file_batteries)
    houses_locs: loc_type = open_file(file_houses)

    create_grid(batteries_locs, houses_locs)


def open_file(filename: str) -> loc_type:
    """
    reads csv files of the location and capacity of the houses
    and batteries
    Pre: filename is a str and leads to valid csv file
    Post: returns loc_type, consisting of x and y coordinates and
          the capacity/output of the battery/house
    """

    coords = []

    with open(filename) as f:
        for line in f:
            if line == "positie,capaciteit\n":
                pass
            elif line == "x,y,maxoutput\n":
                pass
            else:
                line = line.replace("\"", "")
                line = line.replace("\n", "")
                values = line.split(",")

                x = int(values[0])
                y = int(values[1])
                capacity = float(values[2])
                    
                coords.append((x, y, capacity))
                
    return coords


def create_grid(batteries: loc_type, houses: loc_type):
    """
    creates 2d array with every battery and house at its correct location
    """

    max_size: tuple(int, int) = find_size(batteries, houses)

    grid: list[list[tuple[str, int]]] = np.zeros((max_size[0], max_size[1]), dtype=tuple)

    for loc in batteries:
        x = loc[0] * 2 + 1
        y = loc[1] * 2 + 1
        cap = loc[2]
        grid[x][y] = ("bat", cap)

    for loc in houses:
        x = loc[0] * 2 + 1
        y = loc[1] * 2 + 1
        output = loc[2]
        grid[x][y] = ("house", output)

    # print entire array in terminal
    np.set_printoptions(threshold=sys.maxsize)

    # mirror rows, so first row now appears lasts
    np.flipud(grid)
    print(grid)


def find_size(batteries: loc_type, houses: loc_type) -> tuple[int, int]:
    """
    Determines how big the grid should be so every object fits on it
    Pre: batteries and houses are iterables with integers in first and second place
    Post: returns heighest x and y value in batteries and houses
    """

    max_x: int = 0
    max_y: int = 0

    all: loc_type = batteries + houses

    for loc in all:
        if loc[0] > max_x:
            max_x = loc[0]
        if loc[1] > max_y:
            max_y = loc[1]

    # change max values to fit our own representation of the data
    max_x = max_x * 2 + 3
    max_y = max_y * 2 + 3

    return (max_x, max_y)

if __name__ == "__main__":
    district: str = "2"
    main(district)