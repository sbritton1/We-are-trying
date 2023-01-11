import numpy as np
import matplotlib.pyplot as plt

from matplotlib.ticker import MultipleLocator, AutoMinorLocator

grid_size = 50

def visualize():
    # show grid lines
    plt.grid(visible=True, axis='both')

    # set limits of grid
    plt.xlim(0, grid_size)
    plt.ylim(0, grid_size)
    # Intervals for major x-ticks
    plt.xaxis.set_major_locator(MultipleLocator(10))    
    # Minor ticks : Automatic filling based on the ytick range                                                                                                                                       
    plt.xaxis.set_minor_locator(AutoMinorLocator()) 

    # set ticks on axes
    plt.xticks(range(grid_size + 1))
    plt.yticks(range(grid_size + 1))


    plt.plot([1, 2, 3, 4])
    plt.plot([4, 3, 2, 1])
    plt.ylabel('some numbers')
    
    plt.show()


if __name__ == "__main__":
    visualize()

