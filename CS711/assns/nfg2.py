# -*- coding: utf-8 -*-
"""final.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1zAVnev5CiRQ1KrEJUWw47iruZFu2Ranc
"""

#importing numpy
import numpy as np

#defining NFG class
class NFG():
  def __init__(self):
    self.gameType = "NFG"
    self.version = 1
    self.isRational = True
    self.name = ""
    self.players = []
    self.strats = []
    self.utils = []

  #preprocess- creates an instance of NFG class, based on input
  def preprocess(self, filename):
    f = open(filename, "r")
    for j, x in enumerate(f):
      if j == 0:
        self.name = x[9:-2]

      elif j == 1:
        for i in range(len(x)):
          if x[i] == '{':
            if self.players == []:
              while x[i] != '}':
                i += 1
                if x[i] == '"':
                  playEnd = x.find('"', i+1)
                  self.players.append(x[i+1:playEnd])
                  i = playEnd + 1

            elif self.strats == []:
              stratEnd = x.find('}', i+1)
              temp = x[i+1:stratEnd]
              self.strats = list(map(int, temp.split()))
              i = stratEnd + 1 
            
      else:
        self.utils = np.fromstring(x, dtype=np.int32, sep = ' ')
        temp = [*self.strats]
        temp.reverse()
        index = [*range(len(self.players)-1,-1,-1),len(self.players)]
        self.utils = self.utils.reshape((*temp, len(self.players))).transpose(*index)

def computeSDS(filename):
  nfg_game = NFG()
  nfg_game.preprocess(filename)

  sdse = []
  for i in range(len(nfg_game.players)):
    ut = nfg_game.utils[...,i]
    ut = ut.swapaxes(-1,i).copy(order='C')
    maxx = -1000000000
    maxind = []
    best = -2

    for l,j in enumerate(np.nditer(ut)):
      if maxx == j:
        maxind.append(l%nfg_game.strats[i])
      elif maxx < j:
        maxind = []
        maxind.append(l%nfg_game.strats[i])
        maxx = j

      if l%nfg_game.strats[i] == nfg_game.strats[i] - 1:
        if len(maxind) != 1:
          break
        else:
          if best == -2:
            best = maxind[0]
          elif best != maxind[0]:
            best = -1
            break
          maxx = -1000000000
          maxind = []
          
    for k in range(nfg_game.strats[i]):
      if k == best:
        sdse.append(1)
      else:
        sdse.append(0)

  return sdse

def computeWDS(filename):
  nfg_game = NFG()
  nfg_game.preprocess(filename)
  
  wdse = []
  for i in range(len(nfg_game.players)):
    ut = nfg_game.utils[...,i]
    ut = ut.swapaxes(-1,i).copy(order='C')
    maxx = -1000000000
    maxind = []
    best = set([_ for _ in range(nfg_game.strats[i])])
    for l,j in enumerate(np.nditer(ut)):
      if maxx == j:
        maxind.append(l%nfg_game.strats[i])
      elif maxx < j:
        maxind = []
        maxind.append(l%nfg_game.strats[i])
        maxx = j

      if l%nfg_game.strats[i] == nfg_game.strats[i] - 1:
        best = best.intersection(maxind)
        if len(best) == 0:
          break
        maxx = -1000000000
        maxind = []

    put = -1

    if len(best) == 1:
      put = best.pop()
    for k in range(nfg_game.strats[i]):
      if k == put:
        wdse.append(1)
      else:
        wdse.append(0)

  return wdse

def computePSNE(filename):
  x = NFG()
  x.preprocess(filename)
  psne = np.zeros_like(x.utils[...,0])

  for p in range(len(x.players)) : 

    up = x.utils[...,p].swapaxes(-1,p)
    maxind =[]
    max = -1000000000
    for i,u in  np.ndenumerate(up) :
      i = list(i)
      i[p],i[-1] = i[-1],i[p]
      if u == max :
        maxind.append(i)

      elif max < u :
        #new max is {u}
        maxind = []
        maxind.append(i)
        #appending {i}  to new array
        max = u

      if i[-1] == x.strats[p] - 1 :
        #maxind is {maxind}
        for ind in maxind :
          #processing {ind} at {psne[tuple(ind)]}
          psne[tuple(ind)]+=1
        
        maxind =[]
        max = -1000000000

  return psne

#testing
for i in range(1,7):
  print(i)
  s=f'g{i}.nfg'
  print(f"SDS= {computeSDS(s)}")
  print(f"WDS= {computeWDS(s)}")
  print(f"PSNE= {computePSNE(s)}")