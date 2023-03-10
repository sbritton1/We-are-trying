import sys
import time
import datetime
from typing import Callable

from code.classes.grid import Grid
from code.algorithms.own_cables.baseline import baseline
from code.algorithms.own_cables.greedy import greedy
from code.algorithms.own_cables.sd_hill_climber import init_sd_hill_climber
from code.algorithms.shared_cables.hill_climber_shared import init_hill_climber_shared
from code.algorithms.shared_cables.baseline_shared import init_baseline_shared
from code.algorithms.shared_cables.sd_hill_climber_shared import init_sd_hill_climber_shared
from code.algorithms.shared_cables.simulated_annealing import init_simulated_annealing
from code.algorithms.shared_cables.plant_propagation import plant_propagation
from code.algorithms.battery_move.hill_climber_battery import init_hill_climber_battery
from code.algorithms.battery_move.clustering import clustering
from code.algorithms.battery_move.clustering_and_hc_battery import clustering_and_hc_battery
from code.visualization.visualization import visualize
from code.export.to_json import to_json


def main(district: str, algorithm_name: str) -> None:
    # load grid
    grid: Grid = Grid(district)

    # get the algorithm and cable type
    algorithm, cable_type = algorithms[algorithm_name]

    # get the time before the algorithm starts
    start_time = time.time()

    # let the algorithm run on the grid
    grid = algorithm(grid)

    # get the time when the algorithm is done
    end_time = time.time()

    # calculate time it took to run algorithm
    time_taken = round(end_time-start_time)

    # print the time
    print(f"Time taken: {datetime.timedelta(seconds=time_taken)} (H:MM:SS)")

    # lay cables and calculate cost accordingly
    if cable_type == "unique":
        grid.lay_unique_cables()
        grid.calc_cost_normal()

    elif cable_type == "shared":
        grid.lay_shared_cables()
        grid.calc_cost_shared()

    # =============== CHOOSE METHOD(S) OF OUTPUT =================

    # converts the output to a JSON file at filepath /results/output.json
    to_json(grid, cable_type)

    # visualises the grid in a matplotlib window
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
        "baseline_shared": (init_baseline_shared, "shared"),
        "greedy_shared": (greedy, "shared"),
        "hill_climber_shared": (init_hill_climber_shared, "shared"),
        "sd_hill_climber_shared": (init_sd_hill_climber_shared, "shared"),
        "simulated_annealing": (init_simulated_annealing, "shared"),
        "plant_propagation": (plant_propagation, "shared"),
        "hill_climber_battery": (init_hill_climber_battery, "shared"),
        "clustering": (clustering, "shared"),
        "clustering_and_hc_battery": (clustering_and_hc_battery, "shared")
        }

    check_usage()

    # read the command-line arguments
    district: str = sys.argv[1]
    algorithm_name: str = sys.argv[2]

    main(district, algorithm_name)
