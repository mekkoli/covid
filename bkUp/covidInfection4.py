# todo:
# add dead cell with prob grey
# handle graph obj inside covidInfection class
# graph display movements
 
import random

# graph tools
import pygame, sys
from time import sleep
from pygame.locals import *
from time import sleep

class covidInfections:
  """
  susceptible, infected, recovered
  s(t) + i(t) + r(t) = N = dimX * dimY
  infected span infection to susceptible at cell distance 1
  1 cicle (day) to make trip and infect neighbouring
  
  world[x][y] = -1 not populated cell
  world[x][y] = 0 susceptible, populated cell
  world[x][y] = n [1 ... infectDuration] infected
  world[x][y] > infectDuration recovered (dead or recover)

  humanDensity: population = dimX * dimY * humanDensity
  infectDuration: cicles or days
  infectionProb: probability to infect some other at distance 1 from you
  socialSeparation: stay at home, wash hands, surgical mask ... : 1 tripProb
  def trip move: go and back
  """
  
  def __init__( self, covidInit ):
    self.isUnaryProb( covidInit["humanDensity"], "uman density" )
    self.isUnaryProb( covidInit["infectProb"], "infection probability" )
    self.isUnaryProb( covidInit["socialSeparation"], "social separation" )
    self.dimX = covidInit["dimX"]
    self.dimY = covidInit["dimY"]
    self.humanDensity = covidInit["humanDensity"]
    self.infectDuration = covidInit["infectDuration"]
    self.infectProb = covidInit["infectProb"]
    self.socialSeparation = covidInit["socialSeparation"]
    self.tripProb = 1 - self.socialSeparation
    self.name = covidInit["dirName"] + "/(x" + str(self.dimX) + " y" + str(self.dimY) + " id" + str(self.infectDuration) + " hd" + str(self.humanDensity) + " ip" + str(self.infectProb) + " ss" + str(self.socialSeparation) + ")"
    self.f=open( self.name + '.csv', "w+")
    self.f.write("cicle; susceptible, infected " + self.name + "\n")
    self.world = []
    self.maxInfected = 0
    # create homes
    for x in range(self.dimX):
      worldRow = []
      for y in range(self.dimY):
        worldRow.append(-1)
      self.world.append(worldRow) 
    self.populate()
    self.cicle = 0

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
      pygame.draw.rect(graphWin, color, (x * DX + FRAME , y * DX + FRAME , DX, DY))
      pygame.display.update()

  def populate(self):
    global graphWin
    self.population = int(self.humanDensity * self.dimX * self.dimY)
    man = 0
    patientZero = False
    while man < self.population:
      x = random.randint( 0, self.dimX -1 )
      y = random.randint( 0, self.dimY -1 )
      if self.world[x][y] == -1 and self.world[x][y] != 1:
        self.world[x][y] = 0 # susceptible and not infected
        if not patientZero:
          patientZero = True
          zeroX = x
          zeroY = y
          self.world[zeroX][zeroY] = 1
        self.drawCell(x,y)
        pygame.draw.circle(graphWin, INFECTED, (zeroX * DX + int(DX / 2) + FRAME, zeroY * DY + int(DY / 2) + FRAME), 10, 1)
        man += 1
    self.susceptible = self.population - 1
    self.infected = 1
    self.recovered = 0
    print("populated, zero patient({},{})".format(zeroX, zeroY))
    sleep(2)

  def trip(self, x, y):
    if self.yesNoAnswer(self.tripProb):
      dx = random.randint(1,self.dimX)
      dy = random.randint(1,self.dimY)
      destX = (x + dx)
      destY = (y + dy)
      self.infectNeighbour(destX, destY)
    return

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
          self.drawCell(x,y)
    return

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

  def cicleWorld(self):
    while self.infected != 0 or self.susceptible != 0: #self.population * 0.1:
      for x in range(self.dimX):
        for y in range(self.dimY):
          if self.world[x][y] > 0:
            self.world[x][y] +=1
            # if is infected may travel
            self.trip(x,y)
          if self.world[x][y] == self.infectDuration:
            # if infectDuration is passed, recovered or dead
            self.infected -= 1
            self.recovered +=1
            self.drawCell(x,y)
      self.cicle += 1
      xlsRow = str(self.cicle) + ";" + str(self.susceptible) + ";" + str(self.infected) + ";\n" 
      if self.susceptible + self.infected + self.recovered != self.population:
        raise Exception("susc + infect + recover must equal to population")
      self.f.write(xlsRow)
      print(xlsRow, end="")
      if self.maxInfected < self.infected:
        self.maxInfected = self.infected
    self.f.close()
    print( "max: " + str(self.maxInfected))
    return


# set up the colors and dims
VOID = (0, 0, 0)              # black desert cell
SUSCEPTIBLE = (255, 255, 255) # white live and susceptible cell
INFECTED = (255, 0, 0)        # red live and infected cell
RECOVERED = (0, 255, 0)       # green live or dead recovered cell
BLUE = (0, 0, 255)            # blue ?
DX = 5
DY = 5
FRAME = 0

init = {
  "fileName": "05covInfect",
  "dirName": "data",
  "dimX": 30, 
  "dimY": 20,
  "infectDuration": 15, 
  "humanDensity": 0.1, 
  "infectProb": 0.5,
  "socialSeparation": 0.2
}  
pygame.init()
graphWin = pygame.display.set_mode((init["dimX"] * (DX+FRAME) , init["dimY"] * (DX+FRAME)), 0, 32)
pygame.display.set_caption('covid infection simulation')
graphWin.fill(VOID)

w=covidInfections(init)
w.cicleWorld()
sleep(10)
pygame.quit()
exit()

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
