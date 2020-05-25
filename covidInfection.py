# git status
# git add file
# git commit -m "msg"
# git push -u master origin
# git diff nomeFile (diff file -1)

# todo:
# graph display movements: line /line, exist line(color) line(/color) ?

import random
import json
import numpy as np

# graph tools
import pygame, sys
from pygame.locals import *

#plot tools
import matplotlib.pyplot as plt
from tkinter import PhotoImage

# set up the colors and dims
VOIDcOL = (0, 0, 0)             # black desert cell
SUSCcOL = (255, 255, 255)       # white live and susceptible cell
INFECTcOL = (255, 0, 0)         # red live and infected cell
RECOVcOL = (0, 255, 0)          # green live or dead recovered cell
DEADcOL = (120, 120, 120)          # grey
LEGENDcOL = (50, 150, 255)      # blue
EVIcOL = (150, 200, 255)        # light blue
DX = 5
DY = 5
FRAME = 10
LEGENDsIZE = 60
TXTsPACE = 10
FONT = "font/FreeMonoBold.ttf"

# covidLife world[x][y] status
VOID = -1
SUSC = 0
DEAD = -2
STARTiNFECT = 1

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
    self.printTerm = covidInit["printTerm"]
    self.init = covidInit
    self.isUnary( covidInit["humanDensity"], "human density" )
    self.isUnary( covidInit["infectProb"], "infection probability" )
    self.isUnary( covidInit["socialSeparation"], "social separation" )
    self.dimX = covidInit["dimX"]
    self.dimY = covidInit["dimY"]
    self.humanDensity = covidInit["humanDensity"]
    self.infectDuration = covidInit["infectDuration"]
    self.infectProb = covidInit["infectProb"]
    self.socialSeparation = covidInit["socialSeparation"]
    self.world = []
    self.maxInfected = 0
    self.cicle = covidInit["cicles"]
    self.population = covidInit["population"]
    self.world = np.full((self.dimX, self.dimY), VOID)

    # dead sim 
    self.deadSim = covidInit["deadSim"]
    self.intensCareAvail = covidInit["intensCareAvail"]
    self.isUnary( covidInit["deadProb"], "dead probability" )
    self.isUnary( covidInit["intensCareAvail"], "relative to population intensive care avaliable" )
    self.deadProb = covidInit["deadProb"]
    self.deadCicles = covidInit["deadCicles"]

    self.moveProb = 1 - self.socialSeparation
    self.name = covidInit["dirName"] + "/(x" + str(self.dimX) + " y" + str(self.dimY) + " id" + str(self.infectDuration) + " hd" + str(self.humanDensity) + " ip" + str(self.infectProb) + " ss" + str(self.socialSeparation) + " dp" + str(self.deadProb) + " dc" + str(self.deadCicles) + " ic" + str(self.intensCareAvail) + ")"
    covidInit["fileName"] = self.name + ".csv"
    self.f=open( self.name + '.csv', "w+")

    if self.deadSim:
      self.f.write("cicle; susceptible; infected; recovered; dead;\n")
    else:
      self.f.write("cicle; susceptible; infected; recovered;\n")

    if self.graph:
      graphRow = "{:12}{:12}{:12}{:12}{:12}{:12}{:6}{:6}".format("cicle", "population", "density", "infectProb", "socialSep", "maxInfected", "dimX", "dimY")
      putText(FRAME, self.dimY*DY+5.5*FRAME, LEGENDcOL, VOIDcOL, graphRow)
      graphRow = "{:12}{:12}{:12}{:12}{:12}{:12}{:6}{:6}".format(str(self.cicle), str(self.population), str(self.humanDensity), str(self.infectProb), str(self.socialSeparation), str(self.maxInfected), str(self.dimX), str(self.dimY))
      putText(FRAME, self.dimY*DY+7*FRAME, LEGENDcOL, VOIDcOL, graphRow)
    self.populate()

  def drawCell(self, x, y):
    global graphWin
    color = None
    if self.world[x][y] == SUSC:
      color = SUSCcOL
    if self.world[x][y] == DEAD:
      color = DEADcOL
    if self.world[x][y] in range (1,self.infectDuration-1):
      color = INFECTcOL
    if self.world[x][y] >= self.infectDuration:
      color = RECOVcOL
    if color != None:
      pygame.draw.rect(worldWin, color, (x * DX + FRAME, y * DX + FRAME, DX, DY))
      pygame.display.update()

  def populate(self):
    if self.graph:
      global worldWin
    self.population = int(self.humanDensity * self.dimX * self.dimY)
    man = 0
    patientZero = False
    while man < self.population:
      x = random.randint( 0, self.dimX -1 )
      y = random.randint( 0, self.dimY -1 )
      if self.world[x][y] == VOID and self.world[x][y] != 1:
        self.world[x][y] = SUSC # susceptible and not infected
        if self.graph:
          self.drawCell(x,y)
        man += 1
        if self.graph:
          graphRow = "{:12}{:12}".format(str(self.cicle), str(man))
          putText(FRAME, self.dimY*DY+7*FRAME, EVIcOL, VOIDcOL, graphRow)
    self.intensCareAvail = self.population * self.intensCareAvail
    self.susceptible = self.population
    self.infected = 0
    self.recovered = 0
    self.cicle = 0
    self.dead = 0

  def move(self, x, y):
    if self.falseOrTrue(self.moveProb):
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
        if self.falseOrTrue(self.infectProb) and self.world[x][y] == SUSC:
          self.world[x][y] = STARTiNFECT
          self.infected += 1
          self.susceptible -=1
          if self.graph:
            self.drawCell(x,y)

  def falseOrTrue( self, prob ):
    self.isUnary(prob, "probability")
    if random.uniform(0,1) <= prob:
      return True
    else:
      return False

  def isUnary(self, prob, msg):
    if prob >= 0 and prob <=1:
      return True
    else:
      str = "{}={} value must be in [0.0, 1.0]".format(msg,prob)
      raise Exception(str) 
      return false

  def placeZeroPatient(self):
    done = False
    while not done:
      x = random.randint(0,self.dimX-1)
      y = random.randint(0,self.dimY-1)
      if self.world[x][y] == SUSC:
        self.world[x][y] = STARTiNFECT
        self.infected += 1
        self.susceptible -= 1
        if self.graph:
          self.drawCell(x,y)
          pygame.draw.circle(worldWin, INFECTcOL, (x * DX + int(DX / 2) + FRAME, y * DY + int(DY / 2) + FRAME), 16, 1)
          pygame.display.update()
        self.infectNeighbour(x, y)
        done=True

  def cicleWorld(self):
    recoveredList=[]
    susceptibleList=[]
    infectedList=[]
    deadList=[]
    cicleList=[]
    self.placeZeroPatient()
    while (self.recovered + self.dead) != self.population: #self.population * 0.1:
      if self.plot:
        recoveredList.append(self.recovered)
        infectedList.append(self.infected)
        susceptibleList.append(self.susceptible)
        deadList.append(self.dead)
        cicleList.append(self.cicle)
      for x in range(self.dimX):
        for y in range(self.dimY):
          if self.world[x][y] > SUSC: # dead and void cell excluded
            self.world[x][y] += 1
            # if is infected and not dead may travel
            self.move(x,y)
            # can dead only if during infection
            if self.deadSim and self.world[x][y] < self.infectDuration:
              if self.infected >= self.intensCareAvail:
                maxDeadCicles = self.deadCicles
              else:
                maxDeadCicles= 1
              for deadCicle in range(maxDeadCicles):
                if self.falseOrTrue(self.deadProb):
                  self.world[x][y] = DEAD
                  self.dead += 1
                  self.infected -= 1
                  if self.graph:
                    self.drawCell(x,y)
                  break # if dead exit 
          if self.world[x][y] == self.infectDuration:
            # if infectDuration is passed, recovered or dead
            self.infected -= 1
            self.recovered += 1
            if self.graph:
              self.drawCell(x,y)

            if self.graph:
              graphRow = "{:12}".format(str(self.cicle))
              putText(FRAME, self.dimY*DY+7*FRAME, EVIcOL, VOIDcOL, graphRow)
              putText(FRAME, self.dimY * DY + 3.4 * FRAME, RECOVcOL, VOIDcOL, format(self.recovered) + "   ")
              putText(FRAME + 7.5*TXTsPACE, self.dimY * DY + 3.4 * FRAME, SUSCcOL, VOIDcOL, format(self.susceptible) + "   ")
              putText(FRAME + 14*TXTsPACE, self.dimY * DY + 3.4 * FRAME, INFECTcOL, VOIDcOL, format(self.infected) + "   ")
              if self.deadSim:
                putText(FRAME + 20.6*TXTsPACE, self.dimY * DY + 3.4 * FRAME, DEADcOL, VOIDcOL, format(self.dead) + "   ")

      self.cicle += 1
      if self.susceptible + self.infected + self.recovered + self.dead != self.population:
        raise Exception("susc + infect + recover +dead must equal to population")
      if self.deadSim:
        xlsRow = str(self.cicle) + ";" + str(self.susceptible) + ";" + str(self.infected) + ";" + str(self.recovered) + ";" + str(self.dead) + ";\n" 
      else:
        xlsRow = str(self.cicle) + ";" + str(self.susceptible) + ";" + str(self.infected) + ";" + str(self.recovered) + ";\n" 
      self.f.write(xlsRow)
      if self.printTerm:
        print(xlsRow, end="")
      if self.maxInfected < self.infected:
        self.maxInfected = self.infected

    self.init["population"] = self.population
    self.init["maxInfected"] = self.maxInfected
    self.init["deads"] = self.dead
    self.init["cicles"] = self.cicle
    if self.graph:
      graphRow = "{:12}{:12}{:12}{:12}{:12}{:12}{:6}{:6}".format(str(self.cicle), str(self.population), str(self.humanDensity), str(self.infectProb), str(self.socialSeparation), str(self.maxInfected), str(self.dimX), str(self.dimY))
      putText(FRAME, self.dimY*DY+7*FRAME, LEGENDcOL, VOIDcOL, graphRow)
    if self.printTerm:
      print(json.dumps(self.init, indent = 2))
    self.f.write(json.dumps(self.init, indent = 2))
    self.f.close()

    #at the end check consistency cells in the world, recovered, 
    void=0
    at15=0
    other=0
    for x in range(self.dimX):
      for y in range(self.dimY):
        if self.world[x][y] == -VOID:
          void+=1
        elif self.world[x][y] == self.infectDuration:
          at15+=1
        else:
          other+=1
    if self.printTerm:
      print("void cells: "+str(void) + "\ncovidLife @infectDuration: "+str(at15), "\ncovidLife @moreInfectDuration: "+str(other))
    
    if self.plot:
      dataPlot = {
        "winTitle":     "covid infections in time",
        "y5Draw":       self.deadSim,
        "xList":        cicleList,
        "y1List":       susceptibleList,
        "y2List":       infectedList,
        "y3List":       recoveredList,
        "y4List":       deadList,
        "y5Value":      self.intensCareAvail,
        "y1Color":      (SUSCcOL[0]/255.0, SUSCcOL[1]/255.0, SUSCcOL[2]/255.0),              # white
        "y2Color":      (INFECTcOL[0]/255.0, INFECTcOL[1]/255.0, INFECTcOL[2]/255.0),        # red
        "y3Color":      (RECOVcOL[0]/255.0, RECOVcOL[1]/255.0, RECOVcOL[2]/255.0),           # green 
        "y4Color":      (DEADcOL[0]/255.0, DEADcOL[1]/255.0, DEADcOL[2]/255.0),              # grey 
        "y5Color":      (1, 1, 0),        # yellow
        "y1Label":      "susceptible",
        "y2Label":      "infected",
        "y3Label":      "recovered",
        "y4Label":      "dead",
        "y5Label":      "intCareAvail",
        "xLabel":       "time [cicles]",
        "yLabel":       "people [n]",
        "legendLoc":    "upper right",
        "legendBox":    (1, 1)
      }
      plot(dataPlot)

def initGraph(dimX, dimY, deadSim):
  global worldWin
  pygame.init()
  worldWin = pygame.display.set_mode((dimX * DX + 2 * FRAME, dimY * DY + 2 * FRAME + LEGENDsIZE), 0, 32)
  pygame.display.set_caption('covid infection simulation')

  programIcon = pygame.image.load('img/covid.png')
  pygame.display.set_icon(programIcon)

  worldWin.fill(VOIDcOL)
  pygame.draw.rect(worldWin, LEGENDcOL, (FRAME-2, FRAME-2, dimX * DX + 4, dimY * DY + 4 ),1)
  xEnd = putText(FRAME, dimY * DY + 2 * FRAME, RECOVcOL, VOIDcOL, 'recovered')
  xEnd = putText(xEnd + TXTsPACE, dimY * DY + 2 * FRAME, SUSCcOL, VOIDcOL, 'suscetpt')
  xEnd = putText(xEnd + TXTsPACE, dimY * DY + 2 * FRAME, INFECTcOL, VOIDcOL, 'infected')
  if deadSim:
    xEnd = putText(xEnd + TXTsPACE, dimY * DY + 2 * FRAME, DEADcOL, VOIDcOL, 'dead')

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
    if (w.falseOrTrue(0.7333)):
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
    "y5Value"       y5Value,
    "y1Color":      (1, 0, 0),
    "y2Color":      (1, 1, 0.5),
    "y3Color":      (1, 0, 0.5),
    "y4Color":      (1, 0, 0.5),
    "y5Color":      (1, 0, 0.5),
    "y1Label":      "socialSep 0.5",
    "y2Label":      "socialSep 0.6",
    "y3Label":      "socialSep 0.6",
    "y4Label":      "socialSep 0.6",
    "y5Label":      "socialSep 0.6",
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

  y5List=np.full((len(dataPlot["y1List"])),dataPlot["y5Value"])
  
  ax = fig.add_subplot(1, 1, 1)
  ax.plot(dataPlot["xList"], dataPlot["y1List"], color=dataPlot["y1Color"], label=dataPlot["y1Label"])
  ax.plot(dataPlot["xList"], dataPlot["y2List"], color=dataPlot["y2Color"], label=dataPlot["y2Label"])
  ax.plot(dataPlot["xList"], dataPlot["y3List"], color=dataPlot["y3Color"], label=dataPlot["y3Label"])
  if dataPlot["y5Draw"]:
    ax.plot(dataPlot["xList"], dataPlot["y4List"], color=dataPlot["y4Color"], label=dataPlot["y4Label"])
    ax.plot(dataPlot["xList"], y5List, color=dataPlot["y5Color"], label=dataPlot["y5Label"])
  ax.legend(loc=dataPlot["legendLoc"], bbox_to_anchor=dataPlot["legendBox"])

  # axis label
  ax.set_xlabel(dataPlot["xLabel"])
  ax.set_ylabel(dataPlot["yLabel"])
  
  plt.show()

def main():
  f=open('covidInfection.json')
  covidWorld = json.load(f)["covidWorld"]
  f.close()

  if covidWorld["graph"]:
    initGraph(covidWorld["dimX"], covidWorld["dimY"], covidWorld["deadSim"])
  w=covidInfections(covidWorld)
  w.cicleWorld()
  while True and covidWorld["graph"]:
    for event in pygame.event.get():
      if event.type == QUIT:
        pygame.quit()
        exit()

if __name__ == "__main__":
    main()
