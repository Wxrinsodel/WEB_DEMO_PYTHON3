import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)
y = np.sin(x)

plt.plot(x, y)

# save the plot as a file

image_name = f"static/images/plot.png"
plt.savefig(image_name)

# plt.show()