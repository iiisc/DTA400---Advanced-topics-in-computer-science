# Älgar föds och dör varje år
# X antal skjuts ihjäl varje år
# Vi varierar antalet skjutna älgar och ser vad som händer med matplotlib

import matplotlib.pyplot as plt
import numpy
#matplotlib inline          #För jupyter notebook avkommentera
import simpy
import random
from matplotlib import pyplot as plt

SIM_TIME = 10
START_KALVAR = 1000 # Älgar räknas som kalvar under sitt första levnadsår
START_VUXNA = 5000 
global VUXNA_STAT
global KALV_STAT
VUXNA_STAT={}
KALV_STAT={}
d={1:'a'}
d={2:'b'}


AVSKJUTNING = 24

class skogen(object):
    def __init__(self, env, antal_vuxna, antal_kalvar):
        self.env = env
        self.vuxna = antal_vuxna
        self.kalvar = antal_kalvar
        self.årlig_avskjutning = 0
        self.mål_avskjutning = self.vuxna * (AVSKJUTNING / 100)

        #Statistik - År 0.
        self.stats_vuxna = [self.vuxna]
        self.stats_kalvar = [self.kalvar]
        self.stats_skjutna = [self.årlig_avskjutning]
        self.stats_mål_avskjutning = [self.mål_avskjutning]

    def __str__(self):
        return f'År: {self.env.now} - Antal vuxna: {int(self.vuxna)} - Antal kalvar: {int(self.kalvar)} - Skjutna älgar: {int(self.årlig_avskjutning)} - Mål skjutna: {int(self.mål_avskjutning)}'
    
    def update_statistics(self):
        """ Lägger till årets värde sist i en lista """
        self.stats_vuxna.append(self.vuxna)
        self.stats_kalvar.append(self.kalvar)
        self.stats_skjutna.append(self.årlig_avskjutning)
        self.stats_mål_avskjutning.append(self.mål_avskjutning)
        VUXNA_STAT[self.env.now] = int(self.vuxna)
        KALV_STAT [self.env.now] = int(self.kalvar)


    def addera(self):
        """ Årlig ökning av antal älgar """ 
        # Fjolårets kalvar flyttas upp till vuxengruppen
        self.vuxna += self.kalvar
        self.kalvar = 0
        # Här föds nya kalvar
        self.kalvar += (self.vuxna/2)
        return

    def minska(self):
        # Naturlig minskning varje år
        #self.vuxna -= (self.vuxna/2)
        return

    def skjuta(self):
        """Avskjutning varje år. Utifrån publicerad data 2022 ca 83 000 skjuts varje år med en estimation av totalt 340 000 älgar. Dvs ca 24%"""
        # Vi förutsätter att avskjutning sker inom +- 10%-enheter från vårt mål på 24%. 
        slump_faktor = random.randint(-10, 10)

        # Uppdaterar två variabler som används i __str__
        self.mål_avskjutning = self.vuxna * (AVSKJUTNING / 100)
        self.årlig_avskjutning = self.vuxna * (AVSKJUTNING + slump_faktor) / 100
        
        # Jaktsäsong
        self.vuxna -= self.vuxna * ((AVSKJUTNING + slump_faktor) / 100)
        return

def cykel(env):
    """ Funktionen simulerar ett år """
    while True:
        skog.addera()
        skog.minska()
        skog.skjuta()
        skog.update_statistics()
        print(skog)
        yield env.timeout(1)

def statistik():
    """ Genererar en graf """
    plt.plot(skog.stats_skjutna, label = "Skjutna älgar")
    plt.plot(skog.stats_mål_avskjutning, label = "Mål skjutna älgar")
    plt.plot(skog.stats_vuxna, label = "Vuxna älgar")
    plt.plot(skog.stats_kalvar, label = "Älgkalvar")

    plt.ylabel("Antal")
    plt.xlabel("År")
    plt.legend()
    plt.grid()
    plt.ylim(0, 50000)
    plt.show()

if __name__ == "__main__":
    env = simpy.Environment()
    skog = skogen(env, START_VUXNA, START_KALVAR)
    env.process(cykel(env))
    env.run(until=SIM_TIME)
    statistik()
