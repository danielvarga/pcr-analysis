import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib

pdcNegative, pdcPositive, pdcUncertain, pdcNotCalculated = 0, 1, 2, 3

filename, = sys.argv[1:]

a = np.load(filename)
calls = a[:, 0]
d = a[:, 1:]
final = d[:, -1]
print(d.shape)


red_patch = mpatches.Patch(color='red', label='COVID positive')
blue_patch = mpatches.Patch(color='blue', label='COVID negative')


aa = a[a[:, 0] < 1.5]
my_cmap = matplotlib.cm.get_cmap("rainbow").copy()
my_cmap.set_under('b')
my_cmap.set_over('r')

plt.scatter(aa[:, -1], aa[:, -1] - aa[:, -11], c=aa[:, 0], cmap=my_cmap, vmin=.001, vmax=1-.001, alpha=0.2)
plt.xlabel("Final value (45)")
plt.ylabel("Final derivative (45-35)")

plt.legend(handles=[red_patch, blue_patch])

plt.show()

n = 20

for call in (pdcNegative, pdcPositive):
    actual = d[calls==call]
    idx = np.random.randint(len(actual), size=n)
    for curve in actual[idx, :]:
        plt.plot(range(45), curve, color="b" if call == pdcNegative else "r")
plt.legend(handles=[red_patch, blue_patch])
plt.show()


plt.hist(final[calls==pdcNegative], bins=100, color="b")
plt.hist(final[calls==pdcPositive], bins=100, color="r")
plt.legend(handles=[red_patch, blue_patch])
plt.show()


plt.hist([final[calls==pdcNegative], final[calls==pdcPositive]], bins=500, color=["blue", "red"], stacked=True)
plt.xlim((0, 5))
plt.legend(handles=[red_patch, blue_patch])
plt.show()
