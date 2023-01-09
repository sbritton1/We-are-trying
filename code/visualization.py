import numpy as np
import matplotlib.pyplot as plt

# show grid lines
plt.grid(visible=True, axis='both')

X = np.linspace(0, 4*np.pi, 1000)
Y = np.sin(X)

fig, ax = plt.subplots()
ax.plot(X, Y)
fig.show()
