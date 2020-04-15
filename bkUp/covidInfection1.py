# fai dimensioni x e y diverse
import random

class covidInfections:
  """
  susceptible, infected, recovered
  s(t) + i(t) + r(t) = N = dim * dim
  infected span infection to susceptible at distance 1
  1 cicle (day) to make trip and infect neighbouring
  
  infectedCicle = -1 not populated cell
  infectedCicle = 0 susceptible
  infectedCicle = n [1,infectDuration] infected
  infectedCicle > infectDuration recovered (dead or recover)

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
      infectDuration = 15, 
      humanDensity = 0.1, 
      infectProb = 0.5,
      socialSeparation = 0.9
    ):
    self.dim = dim
    self.humanDensity = humanDensity
    self.infectDuration = infectDuration
    self.infectProb = infectProb
    self.tripProb = 1 - socialSeparation
    self.f=open(fileName + "(hd=" + str(self.humanDensity) + ")(ip=" + str(self.infectProb) + ")(ss=" + str(socialSeparation) + ').csv', "w+")
    self.f.write("(hd=" + str(self.humanDensity) + ")(ip=" + str(self.infectProb) + ")(ss=" + str(socialSeparation) + ") cicle; susceptible, infected\n")
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
    patientZero = False
    while man < self.population:
      x = random.randint( 0, self.dim -1 )
      y = random.randint( 0, self.dim -1 )
      if self.world[x][y] == -1 and self.world[x][y] != 1:
        self.world[x][y] = 0 # susceptible and not infected
        if not patientZero:
          patientZero = True
          self.world[x][y] = 1
        man += 1
    self.susceptible = self.population - 1
    self.infected = 1
    self.recovered = 0

  def trip(self, x, y):
    if self.yesNoAnswer(self.tripProb):
      dx = random.randint(1,self.dim)
      dy = random.randint(1,self.dim)
      destX = (x + dx)
      destY = (y + dy)
      self.infectNeighbour(destX, destY)
    return

  def infectNeighbour(self, x, y):
    neighbour = { -1, 0, 1 }
    for dx in neighbour:
      for dy in neighbour:
        x = (x + dx) % self.dim
        y = (y + dy) % self.dim
        if self.yesNoAnswer(self.infectProb) and self.world[x][y] == 0:
          self.world[x][y] = 1
          self.infected += 1
          self.susceptible -=1
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
      for x in range(self.dim):
        for y in range(self.dim):
          if self.world[x][y] > 0:
            self.world[x][y] +=1
            # if is infected may travel
            self.trip(x,y)
          if self.world[x][y] == self.infectDuration:
            # if infectDuration is passed, recovered or dead
            self.infected -= 1
            self.recovered +=1
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

w=covidInfections("covInfect")
w.cicleWorld()
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
