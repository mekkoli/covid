# metti x % dim e y % dim solo dentro update infection
import random

class covidInfections:
  """
  susceptible, infected, recovered
  s(t) + i(t) + r(t) = N = dim * dim
  infected span infection to susceptible at distance 1
  1 cicle (day) to make trip and infect neighbouring
  
  infectedCicle = -1 not populated cell
  infectedCicle = 0 susceptible
  infectedCicle = n [1,15] infected
  infectedCicle > 15 recovered (dead or recover)

  humanDensity: population = dim * dim * 0.40
  infectDuration: trips cicles or days
  infectionProb: probability to infect some other at distance 1 from you
  tripProb: ~ social distance:  trip probability, wash hands, sugical mask ... )

  def trip() no move: go and back
  def setState()
  """

  def __init__(
      self, 
      fileName,
      dim = 100, 
      humanDensity = 0.1, 
      infectDuration = 4, 
      infectProb = 0.01, 
      tripProb = 0.1
    ):
    self.f=open(fileName, "w+")
    self.f.write("cicle; susceptible, infected, recovered\n")
    self.dim = dim
    self.humanDensity = humanDensity
    self.infectDuration = infectDuration
    self.infectProb = infectProb
    self.tripProb = tripProb
    self.world = []
    self.maxInfected = 0
    for m in range(self.dim):
      worldRow = []
      for n in range(self.dim):
        worldRow.append(-1)
      self.world.append(worldRow) 
    self.populate()
    self.cicle = 0

  def populate(self):
    self.population = int(self.humanDensity * self.dim * self.dim)
    man = 0
    while man < self.population:
      row = random.randint( 0, self.dim -1 )
      column = random.randint( 0, self.dim -1 )
      if self.world[row][column] == -1:
        self.world[row][column] = 0 # susceptible and not infected
        man += 1
    self.susceptible = self.population
    self.infected = 0
    self.recovered = 0

  def trip(self, x, y):
    if self.yesNoAnswer(self.tripProb):
      dx = random.randint(1,self.dim)
      dy = random.randint(1,self.dim)
      destX = (x + dx) % self.dim
      destY = (y + dy) % self.dim
      self.infectNeighbour(destX, destY)
    return

  def infectNeighbour(self, x, y):
    for dx in range(-1,1):
      for dy in range (-1,1):
        self.updateInfection( (x + dx) % self.dim, (y + dy) % self.dim )

  def updateInfection(self, x, y):
    if self.yesNoAnswer(self.infectProb) and self.world[x][y] >= 0:
      self.world[x][y] += 1   # begin/continue infection
      if self.world[x][y] == 1:
        self.infected += 1
        self.susceptible -=1
      if self.world[x][y] == self.infectDuration:
        self.recovered += 1   # dead or recovered
        self.infected -=1
    return

  def yesNoAnswer( self, prob ):
    """
    if you want True with 75% prob:
      yesNoAnswer( 0.75)
    """
    if (prob > 1 or prob < 0):
      raise Exception("prob must be inside [0,1]")
    if random.uniform(0,1) <= prob:
      return True
    else:
      return False

  def cicleWorld(self):
    while self.infected != 0 or self.susceptible != 0: #self.population * 0.1:
      for row in range(self.dim):
        for column in range(self.dim):
          if self.world[row][column] < self.infectDuration:
            self.trip(row,column)
            #print(str(row) + " " + str(column), end=' - ')
      self.cicle += 1
      xlsRow = str(self.cicle) + ";" + str(self.susceptible) + ";" + str(self.infected) + ";" + str(self.recovered) + ";\n" 
      self.f.write(xlsRow)
      print(xlsRow, end="")
      if self.maxInfected < self.infected:
        self.maxInfected = self.infected
    self.f.close()
    print( self.maxInfected )
    return

w=covidInfections("covidInfentions.csv")
w.cicleWorld()
#f=open("covidInfentions.csv", "w+")
#f.close()
exit()

"""
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
"""
