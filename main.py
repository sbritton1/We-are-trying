import numpy as np

loc_type = list[tuple[int, int, float]]

def main(district: str):
    file_batteries: str = "data/district_" + district + "/district-" + district + "_batteries.csv"
    file_houses: str= "data/district_" + district + "/district-" + district + "_houses.csv"

    batteries_locs: loc_type = open_file(file_batteries)
    houses_locs: loc_type = open_file(file_houses)

    create_grid(batteries_locs, houses_locs)


def open_file(filename: str) -> loc_type:
    coords = []
    
    with open(filename) as f:

        for line in f:
            if line == "\n":
                pass
            elif line == "x,y,maxoutput\n":
                pass
            elif line == "positie,capaciteit\n":
                pass
            else:
                line = line.replace("\"", "")
                line = line.replace("\n", "")
                values = line.split(",")

                x = int(values[0])
                y = int(values[1])
                capacity = float(values[2])

                print(values)
                    
                coords.append((x, y, capacity))
                
    return coords


def create_grid(batteries: loc_type, houses: loc_type):
    max_size: tuple(int, int) = find_size(batteries, houses)

    grid: list[list[tuple[str, int]]] = [[]]

    for loc in batteries:
        x = loc[0] * 2 + 1
        y = loc[1] * 2 + 1
        cap = loc[2]
        grid[x][y] = ("bat", cap)

    print(grid)

def find_size():
    pass

if __name__ == "__main__":
    district: str = "1"
    main(district)