import numpy as np
import sys
from code.classes.grid import Grid
from code.classes.house import House
from code.algorithms.baseline import baseline

loc_type = list[tuple[int, int, float]]


def main(district: str):
    file_batteries: str = "data/district_" + district + "/district-" + district + "_batteries.csv"
    file_houses: str= "data/district_" + district + "/district-" + district + "_houses.csv"

    grid = Grid(district)

    baseline(grid)

if __name__ == "__main__":
    district: str = "2"
    main(district)