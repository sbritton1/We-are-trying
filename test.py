import matplotlib.pyplot as plt
import math

temps = []
for iteration in range(10000):
    temperature = 500 * (0.997 ** iteration) + ((25 / (math.sqrt(int(iteration / 1000)) + 1)) * 0.997 ** (iteration % 1000))
    temps.append(temperature)

plt.plot(list(range(len(temps))), temps)
plt.xlabel("Iteration")
plt.ylabel("Temperature")
plt.show()