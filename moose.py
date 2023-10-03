# Älgar föds och dör varje år
# X antal skjuts ihjäl varje år
# Vi varierar antalet skjutna älgar och ser vad som händer med matplotlib

import simpy

RANDOM_SEED = 25
SIM_TIME = 10
START_KALVAR = 10 # Älgar räknas som kalvar under sitt första levnadsår
START_VUXNA = 10 
ÅRLIG_MINSKNING = 0
ÅRLIG_AVSKJUTNING = 0

class skogen(object):
    def __init__(self, env, antal_vuxna, antal_kalvar):
        self.env = env
        self.vuxna = antal_vuxna
        self.kalvar = antal_kalvar

    def __str__(self):
        return f'År: {self.env.now} - Antal vuxna: {int(self.vuxna)} - Antal kalvar: {self.kalvar}'

    def addera(self):
        self.vuxna += (self.vuxna/2)
        return self.vuxna

    def minska(START_VUXNA):
        pass

    def skjuta(START_VUXNA):
        pass

    def cykla(self):
        
        yield self.env.timeout(1)

def cykel(env):
    while True:
        print(skog)
        skog.addera()
        yield env.timeout(1)


env = simpy.Environment()
skog = skogen(env, START_VUXNA, START_KALVAR)
env.process(cykel(env))
env.run(until=SIM_TIME)