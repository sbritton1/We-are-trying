import sys

from code.visualization.convert_from_JSON import convert_from_JSON
from code.visualization.visualization import visualize

def visualize_json(filepath: str) -> None:
    grid = convert_from_JSON(filepath)

    visualize(grid)

if __name__ == "__main__":
    filepath = sys.argv[1]

    visualize_json(filepath)