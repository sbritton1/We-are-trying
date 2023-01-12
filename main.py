import numpy as np
import sys
from code.classes.grid import Grid
from code.classes.house import House
from code.algorithms.baseline import baseline
from code.visualization.visualization import visualize
from code.export.to_json import to_json

loc_type = list[tuple[int, int, float]]


def main(district: str):
    grid = Grid(district)

    grid = baseline(grid)

    # to_json(grid)

    visualize(grid)


if __name__ == "__main__":
    district: str = "2"
    main(district)