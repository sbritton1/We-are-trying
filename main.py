import numpy as np
import sys
from code.classes.grid import Grid
from code.classes.house import House
from code.algorithms.own_cables.baseline import baseline
from code.algorithms.own_cables.greedy import greedy
from code.algorithms.own_cables.sd_hill_climber import init_sd_hill_climber
from code.algorithms.shared_cables.hill_climber_shared import hill_climber_shared
from code.algorithms.shared_cables.baseline_shared import baseline_shared
from code.algorithms.shared_cables.sd_hill_climber_shared import init_sd_hill_climber_shared
from code.algorithms.shared_cables.simulated_annealing import init_simulated_annealing
from code.visualization.visualization import visualize
from code.export.to_json import to_json

loc_type = list[tuple[int, int, float]]


def main(district: str, algorithm: str) -> None:
    grid = Grid(district)

    solution = choose_algorithm(grid, algorithm)
    grid = solution[0]
    cable_type = solution[1]

    if cable_type == "unique":
        grid.lay_unique_cables()
        grid.calc_cost_normal()
    
    elif cable_type == "shared":
        grid.lay_shared_cables()
        grid.calc_cost_shared()

    # =============== CHOOSE METHOD(S) OF OUTPUT =================
        
    to_json(grid)
    visualize(grid)


def choose_algorithm(grid: Grid, algorithm: str) -> tuple[Grid, str]:
    if algorithm == "baseline":
        grid: Grid = baseline(grid, 1000)
        return grid, "unique"
    elif algorithm == "greedy":
        grid: Grid = greedy(grid)
        return grid, "unique"
    elif algorithm == "sd_hill_climber":
        grid: Grid = init_sd_hill_climber(grid)
        return grid, "unique"

    elif algorithm == "baseline_shared":
        grid: Grid = baseline_shared(grid, 1000)
        return grid, "shared"
    elif algorithm == "hill_climber_shared":
        grid: Grid = hill_climber_shared(grid)
        return grid, "shared"
    elif algorithm == "sd_hill_climber_shared":
        grid: Grid = init_sd_hill_climber(grid)
        return grid, "shared"
    elif algorithm == "simulated_annealing":
        grid: Grid = init_simulated_annealing(grid)
        return grid, "shared"


if __name__ == "__main__":
    algorithms = ["baseline", "greedy", "sd_hill_climber", "baseline_shared", 
                  "hill_climber_shared", "sd_hill_climber_shared", "simulated_annealing"]

    if len(sys.argv) != 3:
        print("Usage: python main.py <district> <algorithm>")
        sys.exit(1)

    elif sys.argv[2] not in algorithms:
        print("Specified algorithm does not exist, existing algorithms are:")
        for algorithm in algorithms:
            print(f"- {algorithm}")
        sys.exit()

    district: str = sys.argv[1]
    algorithm: str = sys.argv[2]

    main(district, algorithm)