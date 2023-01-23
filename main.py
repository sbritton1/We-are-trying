import sys
import time
import datetime
from typing import Callable

from code.classes.grid import Grid
from code.algorithms.own_cables.baseline import baseline
from code.algorithms.own_cables.greedy import greedy
from code.algorithms.own_cables.sd_hill_climber import init_sd_hill_climber
from code.algorithms.shared_cables.hill_climber_shared import init_hill_climber_shared
from code.algorithms.shared_cables.baseline_shared import baseline_shared
from code.algorithms.shared_cables.sd_hill_climber_shared import init_sd_hill_climber_shared
from code.algorithms.shared_cables.simulated_annealing import init_simulated_annealing
from code.algorithms.shared_cables.plant_propagation import plant_propagation
from code.visualization.visualization import visualize
from code.export.to_json import to_json


def main(district: str, algorithm_name: str) -> None:
    # load grid
    grid = Grid(district)

    # get the algorithm and cable type
    algorithm, cable_type = algorithms[algorithm_name]

    start_time = time.time()
    # let the algorithm run on the grid
    grid = algorithm(grid)
    end_time = time.time()

    print(f"Time taken: {datetime.timedelta(seconds=round(end_time-start_time))} (H:MM:SS)")

    # lay cables and calculate cost accordingly
    if cable_type == "unique":
        grid.lay_unique_cables()
        grid.calc_cost_normal()

    elif cable_type == "shared":
        grid.lay_shared_cables()
        grid.calc_cost_shared()

    # =============== CHOOSE METHOD(S) OF OUTPUT =================

    to_json(grid)
    visualize(grid)



def check_usage() -> None:
    if len(sys.argv) != 3:
        print("Usage: python main.py <district> <algorithm>")
        sys.exit(1)

    elif sys.argv[2] not in algorithms.keys():
        print("Specified algorithm does not exist, existing algorithms are:")
        for algorithm in algorithms.keys():
            print(f"- {algorithm}")
        sys.exit()


if __name__ == "__main__":
    
    # set the algorithms and their cable type in a dictionary
    algorithms: dict[str, tuple[Callable, str]] = {
        "baseline": (baseline, "unique"),
        "greedy": (greedy, "unique"),
        "sd_hill_climber": (init_sd_hill_climber, "unique"),
        "baseline_shared": (baseline_shared, "shared"),
        "greedy_shared": (greedy, "shared"),
        "hill_climber_shared": (init_hill_climber_shared, "shared"),
        "sd_hill_climber_shared": (init_sd_hill_climber_shared, "shared"),
        "simulated_annealing": (init_simulated_annealing, "shared"),
        "plant_propagation": (plant_propagation, "shared")
    }

    check_usage()

    # read the command-line arguments
    district: str = sys.argv[1]
    algorithm_name: str = sys.argv[2]

    main(district, algorithm_name)
