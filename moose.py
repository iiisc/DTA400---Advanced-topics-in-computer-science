# Älgar föds och dör varje år
# X antal skjuts ihjäl varje år
# Vi varierar antalet skjutna älgar och ser vad som händer med matplotlib

import matplotlib.pyplot as plt
import numpy
#matplotlib inline          #För jupyter notebook avkommentera
import simpy

SIM_TIME = 10
START_KALVAR = 1000 # Älgar räknas som kalvar under sitt första levnadsår
START_VUXNA = 5000 
global VUXNA_STAT
global KALV_STAT
VUXNA_STAT={}
KALV_STAT={}
d={1:'a'}
d={2:'b'}
for i in d:
    print(d[i])

class skogen(object):
    def __init__(self, env, antal_vuxna, antal_kalvar):
        self.env = env
        self.vuxna = antal_vuxna
        self.kalvar = antal_kalvar

    def __str__(self):
        VUXNA_STAT[self.env.now] = int(self.vuxna)
        KALV_STAT [self.env.now] = int(self.kalvar)

        return f'År: {self.env.now} - Antal vuxna: {int(self.vuxna)} - Antal kalvar: {int(self.kalvar)}'

    def addera(self):
        # Fjolårets kalvar flyttas upp till vuxengruppen
        self.vuxna += self.kalvar
        self.kalvar = 0
        # Här föds nya kalvar
        self.kalvar += (self.vuxna/2)
        return

    def minska(self):
        # Naturlig minskning varje år
        self.vuxna -= (self.vuxna/2)
        return

    def skjuta(self):
        # Avskjutning varje år
        return

def cykel(env):
    # Funktionen simulerar 1 år.
    while True:
        print(skog)
        skog.addera()
        skog.minska()
        skog.skjuta()
        yield env.timeout(1)


env = simpy.Environment()
skog = skogen(env, START_VUXNA, START_KALVAR)
env.process(cykel(env))
env.run(until=SIM_TIME)
print(VUXNA_STAT)


plt.title("Älgar")
plt.xlabel("Simulerade år")
plt.ylabel("Antal Älgar")           
plt.plot(VUXNA_STAT.keys(),VUXNA_STAT.values())
plt.plot(KALV_STAT.keys(),KALV_STAT.values())
plt.scatter(VUXNA_STAT.keys(),VUXNA_STAT.values())
plt.scatter(KALV_STAT.keys(),KAL5V_STAT.values())

plt.show()