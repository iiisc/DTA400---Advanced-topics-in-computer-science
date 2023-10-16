# Älgar föds och dör varje år
# X antal skjuts ihjäl varje år
# Vi varierar antalet skjutna älgar och ser vad som händer med matplotlib

import matplotlib.pyplot as plt
import numpy
#matplotlib inline          #För jupyter notebook avkommentera
import simpy
import random
from matplotlib import pyplot as plt
import customtkinter

SIM_TIME = 40
START_KALVAR = 1000 # Älgar räknas som kalvar under sitt första levnadsår
START_VUXNA = 5000 
global VUXNA_STAT
global KALV_STAT
VUXNA_STAT={}
KALV_STAT={}

#AVSKJUTNING = 24 # Uttryckt i % av totala populationen, dvs vuxna + kalvar. Dock bara vuxna som blir skjutna. 

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
        if int(self.vuxna) < 0 :
            self.vuxna=0
        self.stats_vuxna.append(self.vuxna)
        self.stats_kalvar.append(self.kalvar)
        self.stats_skjutna.append(self.årlig_avskjutning)
        self.stats_mål_avskjutning.append(self.mål_avskjutning)
       

    def addera(self):
        """ Årlig ökning av antal älgar """ 
        # Fjolårets kalvar flyttas upp till vuxengruppen
        self.vuxna += self.kalvar
        self.kalvar = 0
        # Här föds nya kalvar. I genomsnitt räknar vi med att varje älgko (givet 50% honor) föder 1 älgkalv. 
        self.kalvar += (self.vuxna/2)
        return

    def minska(self):
        # Naturlig minskning varje år 
        #Genomsnittsåldern är 15-25 år för en europeisk älg
        naturligtDöda=self.vuxna/20
        self.vuxna -= naturligtDöda
        return

    def skjuta(self):
        """Avskjutning varje år. Utifrån publicerad data 2022 ca 83 000 skjuts varje år med en estimation av totalt 340 000 älgar. Dvs ca 24%"""
        # Vi förutsätter att avskjutning sker inom +- 10%-enheter från vårt mål på 24%. 
        slump_faktor = random.randint(-10, 10)

        # Uppdaterar två variabler som används i __str__
        self.mål_avskjutning = (self.vuxna + self.kalvar) * (AVSKJUTNING / 100)
        avskjutningsProcentSlump=(AVSKJUTNING + slump_faktor) 
        if avskjutningsProcentSlump > 100:        #Kontroll då det inte går att skjuta mer än 100 procent av populationen
            avskjutningsProcentSlump=100
        self.årlig_avskjutning = (self.vuxna + self.kalvar) * avskjutningsProcentSlump / 100

        print("Verklig procent i avskjutning ", avskjutningsProcentSlump)

        
        
        # Jaktsäsong
        self.vuxna -= (self.vuxna + self.kalvar) * ((avskjutningsProcentSlump) / 100)
        return

def cykel(env):
    """ Funktionen simulerar ett år """
    while True:
        skog.addera()
        skog.skjuta()
        skog.minska()
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
    #plt.ylim(0, 50000)
    plt.show()
""" 
if __name__ == "__main__":
    env = simpy.Environment()
    skog = skogen(env, START_VUXNA, START_KALVAR)
    env.process(cykel(env))
    env.run(until=SIM_TIME)
    statistik()
 """

def runSimulation():
    plt.close()
    if not startAlg.get():
        startAlg.insert(0, 1000)
    if not skjutMal.get():
        skjutMal.insert(0, 24)
    if not simuleringsTid.get():
        simuleringsTid.insert(0, 10)
    SIM_TIME=int(simuleringsTid.get())
    START_VUXNA = int(startAlg.get()) 
    global AVSKJUTNING
    AVSKJUTNING =int(skjutMal.get())

    
        
    test=skjutMal.get()
    print("Kör simulering")
    print("Start vuxna ", START_VUXNA)

    print("Procent avskjutning ",AVSKJUTNING)

    print("Simuleringstid ",SIM_TIME)

    env = simpy.Environment()
    global skog
    skog = skogen(env, START_VUXNA, START_KALVAR)
    env.process(cykel(env))
    env.run(until=SIM_TIME)
    statistik()



##  GUI
customtkinter.set_appearance_mode("system")

customtkinter.set_default_color_theme("dark-blue")

root=customtkinter.CTk()
root.geometry("500x350")



frame=customtkinter.CTkFrame(master=root)
frame.pack(pady=20,padx=60,fill="both",expand=True)
label=customtkinter.CTkLabel(master=frame, text="Älgar", font=("helvetica",30))
label.pack(pady=10,padx=20)



startAlg =customtkinter.CTkEntry(master=frame,placeholder_text="Antal startälgar")
startAlg.pack(padx=10,pady=12)

skjutMal =customtkinter.CTkEntry(master=frame,placeholder_text="Mål att skjuta i %")
skjutMal.pack(padx=10,pady=12)

simuleringsTid = customtkinter.CTkEntry(master=frame,placeholder_text="Simulerade år",)
simuleringsTid.pack(pady=12,padx=10)

startKnapp=customtkinter.CTkButton(master=frame,text="Starta simulering",command=runSimulation)
startKnapp.pack(pady=12,padx=10)




root.mainloop()