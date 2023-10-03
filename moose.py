# Älgar föds och dör varje år
# X antal skjuts ihjäl varje år
# Vi varierar antalet skjutna älgar och ser vad som händer med matplotlib

import simpy

RANDOM_SEED = 25
SIM_TIME = 300
START_ÄLGAR = 100

KALVAR = 0 # Älgar räknas som kalvar under sitt första levnadsår
VUXNA = 0 
ÅRLIG_ÖKNING = (VUXNA / 2) * 1.3 # Vi antar att hälften av alla vuxna älgar är älgkor
ÅRLIG_MINSKNING = 0
ÅRLIG_AVSKJUTNING = 0

class skogen(object):
    def __init__(self, env):
        self.env = env

    def addera(VUXNA):
        VUXNA += ÅRLIG_ÖKNING 

    def minska(VUXNA):
        pass

    def skjuta(VUXNA):
        pass

def setup(env):
    skog = skogen(env)

    while True:
        pass


env = simpy.Environment()
env.process(setup(env))
env.run(until=SIM_TIME)


