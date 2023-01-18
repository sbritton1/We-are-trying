import numpy as np
import sys
from code.classes.grid import Grid
from code.classes.house import House
from code.algorithms.baseline import baseline
from code.algorithms.greedy import greedy
from code.algorithms.sd_hill_climber import init_sd_hill_climber
from code.visualization.visualization import visualize
from code.export.to_json import to_json

loc_type = list[tuple[int, int, float]]


def main(district: str):
    grid = Grid(district)

    # grid = baseline(grid)
    # grid = greedy(grid)
    grid = init_sd_hill_climber(grid)

    # ================ CHOOSE METHOD OF CABLES ===============
    # METHOD: non-shared cables
    for house in grid.houses:
        house.lay_cables()

    grid.calc_cost_normal()
    
    # METHOD: shared cables
    # for battery in grid.batteries:
    #    battery.lay_shared_cables()
    # 
    # grid.calc_cost_shared()

    # =============== CHOOSE METHOD(S) OF OUTPUT =================

    #grid.calc_cost_shared()
        
    to_json(grid)
    visualize(grid)


if __name__ == "__main__":
    # choose district
    district: str = "2"

    main(district)