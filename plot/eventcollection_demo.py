"""
====================
EventCollection Demo
====================

Plot two curves, then use EventCollections to mark the locations of the x
and y data points on the respective axes for each curve
"""

import matplotlib.pyplot as plt
from matplotlib.collections import EventCollection
import numpy as np

# Fixing random state for reproducibility
np.random.seed(19680801)

# create random data
xdata = np.random.random([2, 10]) # matrix[0..1][0..9]

# split the data into two parts
xdata1 = xdata[0, :]
xdata2 = xdata[1, :]

# sort the data so it makes clean curves
xdata1.sort() # x data
xdata2.sort()

# create some y data points
ydata1 = xdata1 ** 2  # ydata
ydata2 = 1 - xdata2 ** 3

# dark theme
plt.style.use('dark_background')

# plot the data
fig = plt.figure("azz")

ax = fig.add_subplot(1, 1, 1)
ax.plot(xdata1, ydata1, color='tab:red')
ax.plot(xdata2, ydata2, color='tab:orange')

# create the events marking the x data points
xevents1 = EventCollection(xdata1, color='tab:blue', linelength=0.05)
xevents2 = EventCollection(xdata2, color='tab:orange', linelength=0.05)

# create the events marking the y data points
yevents1 = EventCollection(ydata1, color='tab:blue', linelength=0.05,
                           orientation='vertical')
yevents2 = EventCollection(ydata2, color='tab:orange', linelength=0.05,
                           orientation='vertical')


# add the events to the x axis
ax.add_collection(xevents1)
ax.add_collection(xevents2)

# add the events to the y axis
ax.add_collection(yevents1)
ax.add_collection(yevents2)


# set the limits
ax.set_xlim([0, 1])
ax.set_ylim([0, 1])

# axis label
ax.set_xlabel('days')
ax.set_ylabel('recovered')

ax.set_title('line plot with data points')

# display the plot
plt.show()
