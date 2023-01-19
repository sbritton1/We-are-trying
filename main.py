import numpy as np
import sys
from code.classes.grid import Grid
from code.classes.house import House
from code.algorithms.own_cables.baseline import baseline
from code.algorithms.own_cables.greedy import greedy
from code.algorithms.own_cables.sd_hill_climber import init_sd_hill_climber
from code.algorithms.shared_cables.testen_algo import testen_algo
from code.algorithms.shared_cables.baseline_shared import baseline_shared
from code.algorithms.shared_cables.sd_hill_climber_shared import init_sd_hill_climber_shared
from code.algorithms.shared_cables.simulated_annealing import init_simulated_annealing
from code.visualization.visualization import visualize
from code.export.to_json import to_json

loc_type = list[tuple[int, int, float]]


def main(district: str):
    grid = Grid(district)

    # ================ CHOOSE ALGORITHM ======================

    # grid = baseline(grid, 10000)
    # grid = greedy(grid)
    # grid = init_sd_hill_climber(grid)

    # grid = baseline_shared(grid, 1000)
    # grid = init_sd_hill_climber_shared(grid)
    grid = init_simulated_annealing(grid)
    # grid = testen_algo(grid)

    # ================ CHOOSE METHOD OF CABLES ===============
    
    # METHOD: non-shared cables
    # grid.lay_unique_cables()
    # grid.calc_cost_normal()
    
    # METHOD: shared cables
    grid.lay_shared_cables()
    grid.calc_cost_shared()

    # =============== CHOOSE METHOD(S) OF OUTPUT =================
        
    to_json(grid)
    visualize(grid)


if __name__ == "__main__":
    # choose district
    district: str = "1"

    main(district)