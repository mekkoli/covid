import matplotlib.pyplot as plt
import numpy as np

def plot(dataPlot):
  """
  dataPlot = {
    "winTitle":     "covid infections in time",
    "xList":        xdata1,
    "y1List":       ydata1,
    "y2List":       ydata2,
    "y1Color":      (1, 0, 0),
    "y2Color":      (1, 1, 0.5),
    "y1Label":      "socialSep 0.5",
    "y2Label":      "socialSep 0.6",
    "xLabel":       "time [cicles]",
    "yLabel":       "infected [n]",
    "legendLoc":    "upper left",
    "legendBox":    (-0.01, 1.16)
  }
  """
  # dark theme
  plt.style.use('dark_background')
  plt.rcParams['toolbar'] = 'None' 

  # plot the data
  fig = plt.figure(dataPlot["winTitle"])
  ax = fig.add_subplot(1, 1, 1)
  ax.plot(dataPlot["xList"], dataPlot["y1List"], color=dataPlot["y1Color"], label=dataPlot["y1Label"])
  ax.plot(dataPlot["xList"], dataPlot["y2List"], color=dataPlot["y2Color"], label=dataPlot["y2Label"])
  ax.legend(loc=dataPlot["legendLoc"], bbox_to_anchor=dataPlot["legendBox"])

  # axis label
  ax.set_xlabel(dataPlot["xLabel"])
  ax.set_ylabel(dataPlot["yLabel"])
  
  plt.show()

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

dataPlot = {
    "winTitle":     "covid infections in time",
    "xList":        xdata1,
    "y1List":       ydata1,
    "y2List":       ydata2,
    "y1Color":      (1, 0, 0),
    "y2Color":      (1, 1, 0.5),
    "y1Label":      "socialSep 0.5",
    "y2Label":      "socialSep 0.6",
    "xLabel":       "time [cicles]",
    "yLabel":       "infected [n]",
    "legendLoc":    "upper left",
    "legendBox":    (-0.01, 1.16)
  }
plot(dataPlot)
