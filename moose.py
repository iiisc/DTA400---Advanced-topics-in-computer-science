# Älgar föds och dör varje år
# X antal skjuts ihjäl varje år
# Vi varierar antalet skjutna älgar och ser vad som händer med matplotlib

import simpy

SIM_TIME = 10
START_KALVAR = 1000 # Älgar räknas som kalvar under sitt första levnadsår
START_VUXNA = 5000 
ÅRLIG_MINSKNING = 0
ÅRLIG_AVSKJUTNING = 0

class skogen(object):
    def __init__(self, env, antal_vuxna, antal_kalvar):
        self.env = env
        self.vuxna = antal_vuxna
        self.kalvar = antal_kalvar

    def __str__(self):
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