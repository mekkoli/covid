# git
# git add file
# git commit -m "msg"
# git push master origin
# todo:
# add dead cell with prob grey
# add compare 2 world
# graph display movements: line /line, exist line(color) line(/color) ?

import random
import json

# graph tools
import pygame, sys
from pygame.locals import *

#plot tools
import matplotlib.pyplot as plt
import numpy as np
from tkinter import PhotoImage

# set up the colors and dims
VOID = (0, 0, 0)              # black desert cell
MOVE = (0, 0, 0, 0)           # grey dead
SUSCEPTIBLE = (255, 255, 255) # white live and susceptible cell
INFECTED = (255, 0, 0)        # red live and infected cell
RECOVERED = (0, 255, 0)       # green live or dead recovered cell
LEGEND = (50, 150, 255)       # blue
EVIDENT = (150, 200, 255)     # light blue
DX = 5
DY = 5
FRAME = 10
LEGENDsIZE = 60
TXTsPACE = 10
"copied in active directory"
FONT = "font/FreeMonoBold.ttf"

class covidInfections:
  """
  susceptible, infected, recovered
  s(t) + i(t) + r(t) = N = dimX * dimY
  infected span infection to susceptible at cell distance 1
  1 cicle (day) to make move and infect neighbouring
  
  world[x][y] = -1 not populated cell
  world[x][y] = 0 susceptible, populated cell
  world[x][y] = n [1 ... infectDuration] infected
  world[x][y] > infectDuration recovered (dead or recover)

  humanDensity: population = dimX * dimY * humanDensity
  infectDuration: cicles or days
  infectionProb: probability to infect some other at distance 1 from you
  socialSeparation: stay at home, wash hands, surgical mask ... : 1 moveProb
  def move move: go and back
  """
  def __init__( self, covidInit ):
    self.graph = covidInit["graph"]
    self.plot = covidInit["plot"]
    self.init = covidInit
    self.isUnaryProb( covidInit["humanDensity"], "uman density" )
    self.isUnaryProb( covidInit["infectProb"], "infection probability" )
    self.isUnaryProb( covidInit["socialSeparation"], "social separation" )
    self.dimX = covidInit["dimX"]
    self.dimY = covidInit["dimY"]
    self.humanDensity = covidInit["humanDensity"]
    self.infectDuration = covidInit["infectDuration"]
    self.infectProb = covidInit["infectProb"]
    self.socialSeparation = covidInit["socialSeparation"]
    self.moveProb = 1 - self.socialSeparation
    self.name = covidInit["dirName"] + "/(x" + str(self.dimX) + " y" + str(self.dimY) + " id" + str(self.infectDuration) + " hd" + str(self.humanDensity) + " ip" + str(self.infectProb) + " ss" + str(self.socialSeparation) + ")"
    covidInit["fileName"] = self.name + ".csv"
    self.f=open( self.name + '.csv', "w+")
    self.f.write("cicle; susceptible, infected " + self.name + "\n")
    self.world = []
    self.maxInfected = 0
    self.cicle = covidInit["cicles"]
    self.population = covidInit["population"]
    # create homes
    for x in range(self.dimX):
      worldRow = []
      for y in range(self.dimY):
        worldRow.append(-1)
      self.world.append(worldRow) 
    if self.graph:
      graphRow = "{:12}{:12}{:12}{:12}{:12}{:12}{:6}{:6}".format("cicle", "population", "density", "infectProb", "socialSep", "maxInfected", "dimX", "dimY")
      putText(FRAME, self.dimY*DY+5.5*FRAME, LEGEND, VOID, graphRow)
      graphRow = "{:12}{:12}{:12}{:12}{:12}{:12}{:6}{:6}".format(str(self.cicle), str(self.population), str(self.humanDensity), str(self.infectProb), str(self.socialSeparation), str(self.maxInfected), str(self.dimX), str(self.dimY))
      putText(FRAME, self.dimY*DY+7*FRAME, LEGEND, VOID, graphRow)
    self.populate()

  def drawCell(self, x, y):
    global graphWin
    color = None
    if self.world[x][y] == 0:
      color = SUSCEPTIBLE
    if self.world[x][y] in range (1,self.infectDuration-1):
      color = INFECTED
    if self.world[x][y] >= self.infectDuration:
      color = RECOVERED
    if color != None:
      pygame.draw.rect(worldWin, color, (x * DX + FRAME, y * DX + FRAME, DX, DY))
      pygame.display.update()

  def populate(self):
    if self.graph:
      global worldWin
    self.population = int(self.humanDensity * self.dimX * self.dimY)
    print("population: " + str(self.population))
    man = 0
    patientZero = False
    while man < self.population:
      x = random.randint( 0, self.dimX -1 )
      y = random.randint( 0, self.dimY -1 )
      if self.world[x][y] == -1 and self.world[x][y] != 1:
        self.world[x][y] = 0 # susceptible and not infected
        if self.graph:
          self.drawCell(x,y)
        man += 1
        if self.graph:
          graphRow = "{:12}{:12}".format(str(self.cicle), str(man))
          putText(FRAME, self.dimY*DY+7*FRAME, EVIDENT, VOID, graphRow)
    self.susceptible = self.population
    self.infected = 0
    self.recovered = 0
    self.cicle = 0

  def move(self, x, y):
    if self.yesNoAnswer(self.moveProb):
      dx = random.randint(1,self.dimX-1)
      dy = random.randint(1,self.dimY-1)
      destX = (x + dx)
      destY = (y + dy)
      self.infectNeighbour(destX, destY)
      destX = destX % self.dimX
      destY = destY % self.dimY

  def infectNeighbour(self, x, y):
    neighbour = { -1, 0, 1 }
    for dx in neighbour:
      for dy in neighbour:
        x = (x + dx) % self.dimX
        y = (y + dy) % self.dimY
        if self.yesNoAnswer(self.infectProb) and self.world[x][y] == 0:
          self.world[x][y] = 1
          self.infected += 1
          self.susceptible -=1
          if self.graph:
            self.drawCell(x,y)

  def yesNoAnswer( self, prob ):
    """
    if you want True with 75% prob:
      yesNoAnswer( 0.75)
    """
    if (prob > 1 or prob < 0):
      raise Exception("prob must be in [0.0, 1.0]")
    if random.uniform(0,1) <= prob:
      return True
    else:
      return False

  def isUnaryProb(self, prob, msg):
    if prob >= 0 and prob <=1:
      return True
    else:
      str = "{}={} prob must be in [0.0, 1.0]".format(msg,prob)
      raise Exception(str) 
      return false

  def placeZeroPatient(self):
    done = False
    while not done:
      x = random.randint(0,self.dimX-1)
      y = random.randint(0,self.dimY-1)
      if self.world[x][y] == 0:
        self.world[x][y] = 1
        self.infected += 1
        self.susceptible -= 1
        if self.graph:
          self.drawCell(x,y)
          pygame.draw.circle(worldWin, LEGEND, (x * DX + int(DX / 2) + FRAME, y * DY + int(DY / 2) + FRAME), 16, 2)
          pygame.display.update()
        self.infectNeighbour(x, y)
        done=True

  def cicleWorld(self):
    recoveredList=[]
    susceptibleList=[]
    infectedList=[]
    cicleList=[]
    self.placeZeroPatient()
    while self.recovered != self.population: #self.population * 0.1:
      if self.plot:
        recoveredList.append(self.recovered)
        infectedList.append(self.infected)
        susceptibleList.append(self.susceptible)
        cicleList.append(self.cicle)
      for x in range(self.dimX):
        for y in range(self.dimY):
          if self.world[x][y] > 0:
            self.world[x][y] +=1
            # if is infected may travel
            self.move(x,y)
          if self.world[x][y] == self.infectDuration:
            # if infectDuration is passed, recovered or dead
            self.infected -= 1
            self.recovered +=1
            if self.graph:
              self.drawCell(x,y)

            if self.graph:
              graphRow = "{:12}".format(str(self.cicle))
              putText(FRAME, self.dimY*DY+7*FRAME, EVIDENT, VOID, graphRow)
              putText(FRAME, self.dimY * DY + 3.4 * FRAME, RECOVERED, VOID, format(self.recovered) + "   ")
              putText(FRAME + 7.5*TXTsPACE, self.dimY * DY + 3.4 * FRAME, SUSCEPTIBLE, VOID, format(self.susceptible) + "   ")
              putText(FRAME + 14*TXTsPACE, self.dimY * DY + 3.4 * FRAME, INFECTED, VOID, format(self.infected) + "   ")

      self.cicle += 1
      if self.susceptible + self.infected + self.recovered != self.population:
        raise Exception("susc + infect + recover must equal to population")
      xlsRow = str(self.cicle) + ";" + str(self.susceptible) + ";" + str(self.infected) + ";\n" 
      self.f.write(xlsRow)
      print(xlsRow, end="")
      if self.maxInfected < self.infected:
        self.maxInfected = self.infected

    self.init["population"] = self.population
    self.init["maxInfected"] = self.maxInfected
    self.init["cicles"] = self.cicle
    if self.graph:
      graphRow = "{:12}{:12}{:12}{:12}{:12}{:12}{:6}{:6}".format(str(self.cicle), str(self.population), str(self.humanDensity), str(self.infectProb), str(self.socialSeparation), str(self.maxInfected), str(self.dimX), str(self.dimY))
      putText(FRAME, self.dimY*DY+7*FRAME, LEGEND, VOID, graphRow)
    print(json.dumps(self.init, indent = 2))
    self.f.write(json.dumps(self.init, indent = 2))
    self.f.close()

    if self.plot:
      dataPlot = {
        "winTitle":     "covid infections in time",
        "xList":        cicleList,
        "y1List":       susceptibleList,
        "y2List":       infectedList,
        "y3List":       recoveredList,
        "y1Color":      (1, 1, 1),
        "y2Color":      (1, 0, 0),
        "y3Color":      (0, 1, 0),
        "y1Label":      "susceptible",
        "y2Label":      "infected",
        "y3Label":      "recovered",
        "xLabel":       "time [cicles]",
        "yLabel":       "people [n]",
        "legendLoc":    "upper left",
        "legendBox":    (0.7, 0.5)
      }
      plot(dataPlot)

def initGraph(dimX, dimY):
  global worldWin
  pygame.init()
  worldWin = pygame.display.set_mode((dimX * DX + 2 * FRAME, dimY * DY + 2 * FRAME + LEGENDsIZE), 0, 32)
  pygame.display.set_caption('covid infection simulation')

  programIcon = pygame.image.load('img/covid.png')
  pygame.display.set_icon(programIcon)

  worldWin.fill(VOID)
  pygame.draw.rect(worldWin, LEGEND, (FRAME-2, FRAME-2, dimX * DX + 4, dimY * DY + 4 ),1)
  xEnd = putText(FRAME, dimY * DY + 2 * FRAME, RECOVERED, VOID, 'recovered')
  xEnd = putText(xEnd + TXTsPACE, dimY * DY + 2 * FRAME, SUSCEPTIBLE, VOID, 'suscetpt')
  xEnd = putText(xEnd + TXTsPACE, dimY * DY + 2 * FRAME, INFECTED, VOID, 'infected')

def putText(x, y, color, paper, text):
  font = pygame.font.Font(FONT, 12)
  text = font.render(text, True, color, paper)
  textRect = text.get_rect()
  textRect.center = (x-2+textRect.width//2, y)
  worldWin.blit(text, textRect)
  pygame.display.update()
  return x+textRect.width

def testProb():
  p=0
  for m in range(w.dim):
    for n in range(w.dim):
      if w.world[m][n] == 0:
        p += 1
  print( p, w.dim * w.dim ) 
  counts = 0 
  shots = 1000000
  for n in range(1,shots):
    if (w.yesNoAnswer(0.7333)):
      counts += 1
  print(counts/shots*100.0)

def plot(dataPlot):
  """
  dataPlot = {
    "winTitle":     "covid infections in time",
    "xList":        xdata1,
    "y1List":       ydata1,
    "y2List":       ydata2,
    "y3List":       ydata3,
    "y1Color":      (1, 0, 0),
    "y2Color":      (1, 1, 0.5),
    "y3Color":      (1, 0, 0.5),
    "y1Label":      "socialSep 0.5",
    "y2Label":      "socialSep 0.6",
    "y3Label":      "socialSep 0.6",
    "xLabel":       "time [cicles]",
    "yLabel":       "people [n]",
    "legendLoc":    "upper left",
    "legendBox":    (-0.01, 1.16)
  }
  """
  # dark theme
  plt.style.use('dark_background')
  plt.rcParams['toolbar'] = 'None' 

  # plot the data
  fig = plt.figure(dataPlot["winTitle"])

  # set plt icon
  thismanager = plt.get_current_fig_manager()
  img = PhotoImage(file="img/covidPlot.png")
  thismanager.window.tk.call('wm', 'iconphoto', thismanager.window._w, img)


  ax = fig.add_subplot(1, 1, 1)
  ax.plot(dataPlot["xList"], dataPlot["y1List"], color=dataPlot["y1Color"], label=dataPlot["y1Label"])
  ax.plot(dataPlot["xList"], dataPlot["y2List"], color=dataPlot["y2Color"], label=dataPlot["y2Label"])
  ax.plot(dataPlot["xList"], dataPlot["y3List"], color=dataPlot["y3Color"], label=dataPlot["y3Label"])
  ax.legend(loc=dataPlot["legendLoc"], bbox_to_anchor=dataPlot["legendBox"])

  # axis label
  ax.set_xlabel(dataPlot["xLabel"])
  ax.set_ylabel(dataPlot["yLabel"])
  
  plt.show()

def main():
  with open('covidInfections.json') as f:
    covidWorld = json.load(f)["covidWorld"]
  if covidWorld["graph"]:
    initGraph(covidWorld["dimX"], covidWorld["dimY"])
  w=covidInfections(covidWorld)
  w.cicleWorld()
  while True and covidWorld["graph"]:
    for event in pygame.event.get():
      if event.type == QUIT:
        pygame.quit()
        exit()

if __name__ == "__main__":
    main()
