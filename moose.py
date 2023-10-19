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

class skogen(object):
    def __init__(self, env, antal_vuxna, antal_kalvar):
        self.env = env
        self.vuxna = antal_vuxna
        self.kalvar = antal_kalvar
        self.årlig_avskjutning = 0
        self.mål_avskjutning = self.vuxna * (AVSKJUTNING / 100)
        self.naturlig_död = 0

        #Statistik - År 0.
        self.stats_vuxna = [self.vuxna]
        self.stats_kalvar = [self.kalvar]
        self.stats_skjutna = [self.årlig_avskjutning]
        self.stats_mål_avskjutning = [self.mål_avskjutning]
        self.stats_naturlig_död = [self.naturlig_död]

    def __str__(self):
        return f'År: {self.env.now} - Antal vuxna: {int(self.vuxna)} - Antal kalvar: {int(self.kalvar)} - Skjutna älgar: {int(self.årlig_avskjutning)} - Mål skjutna: {int(self.mål_avskjutning)} - Naturligt döda: {int(self.naturlig_död)} '
    
    def update_statistics(self):
        """ Lägger till årets värde sist i en lista """
        if int(self.vuxna) < 0 :
            self.vuxna=0
        self.stats_vuxna.append(self.vuxna)
        self.stats_kalvar.append(self.kalvar)
        self.stats_skjutna.append(self.årlig_avskjutning)
        self.stats_mål_avskjutning.append(self.mål_avskjutning)
        self.stats_naturlig_död.append(self.naturlig_död)
       
    def addera(self):
        """ Årlig ökning av antal älgar """ 
        # Fjolårets kalvar flyttas upp till vuxengruppen
        self.vuxna += self.kalvar
        self.kalvar = 0
        # Här föds nya kalvar. Hälften av alla älgkor föder en kalv om året vilket är en approximation. 
        self.kalvar += (self.vuxna/3)
        return

    def minska(self):
        """ Naturlig minskning varje år """
        #Genomsnittsåldern är 15-25 år för en europeisk älg
        naturligtDöda=self.vuxna/20
        self.naturlig_död=naturligtDöda
        self.vuxna -= naturligtDöda
        return

    def skjuta(self):
        """Avskjutning varje år. Utifrån publicerad data 2022 ca 83 000 skjuts varje år med en estimation av totalt 340 000 älgar. Dvs ca 24%"""
        # Vi förutsätter att avskjutning sker inom +- 10%-enheter från vårt mål. 
        slump_faktor = random.randint(-10, 10)
        jaktstop = False
        extra_jakt = 0
        
        if self.vuxna > 400000:
            extra_jakt = 30
            slump_faktor += 30
        if self.vuxna < 50000:
            jaktstop = True
            self.mål_avskjutning = 0
            self.årlig_avskjutning = 0

        # Här kommer logik som sköter avskjutning och uppdatering av variabler för statistik. 
        if not jaktstop:
            if (AVSKJUTNING + slump_faktor + extra_jakt) < 100:
                self.mål_avskjutning = self.vuxna * ( (AVSKJUTNING + extra_jakt) / 100)
                self.årlig_avskjutning = self.vuxna * ((AVSKJUTNING + slump_faktor) / 100)
                self.vuxna -= self.vuxna * ((AVSKJUTNING + slump_faktor) / 100)
            else:
                self.mål_avskjutning = self.vuxna
                self.årlig_avskjutning = self.vuxna
                self.vuxna -= self.vuxna
        return

def cykel(env):

    """ Funktionen simulerar ett år """
    while True:
        skog.skjuta()
        if naturligDöd.get() ==1:
            skog.minska()
        skog.addera()
        skog.update_statistics()
        yield env.timeout(1)

def statistik():
    """ Genererar en graf """
    plt.plot(skog.stats_skjutna, label = "Skjutna älgar")
    if showMål.get()==1:
        plt.plot(skog.stats_mål_avskjutning, label = "Mål skjutna älgar")
    plt.plot(skog.stats_vuxna, label = "Vuxna älgar")
    if showKalv.get()==1:
        plt.plot(skog.stats_kalvar, label = "Älgkalvar")
    if showNaturlig.get()==1:
        plt.plot(skog.stats_naturlig_död, label="Naturlig död")

    plt.ylabel("Antal")
    plt.xlabel("År")
    plt.legend()
    plt.grid()
    plt.show()

def runSimulation():
    plt.close()
    # Start variabler om inget anges i input-rutan
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
        
    #print("Kör simulering")
    #print("Start vuxna ", START_VUXNA)
    #print("Procent avskjutning ",AVSKJUTNING)
    #print("Simuleringstid ",SIM_TIME)
    
    env = simpy.Environment()
    global skog
    skog = skogen(env, START_VUXNA, START_KALVAR)
    env.process(cykel(env))
    env.run(until=SIM_TIME)
    statistik()

##  GUI
customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("dark-blue")

global naturligDÖd
global showKalv
global showMål
global showNaturlig

root=customtkinter.CTk()
root.geometry("500x550")

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

naturligDöd = customtkinter.CTkCheckBox(master=frame,text="Räkna med naturlig död")
naturligDöd.pack(pady=12,padx=10)

startKnapp=customtkinter.CTkButton(master=frame,text="Starta simulering",command=runSimulation)
startKnapp.pack(pady=12,padx=10)

showKalv = customtkinter.CTkCheckBox(master=frame,text="Visa kalvstatistik")
showKalv.pack(pady=12,padx=10)
showMål =  customtkinter.CTkCheckBox(master=frame,text="Visa mål")
showMål.pack(pady=12,padx=10)
showNaturlig = customtkinter.CTkCheckBox(master=frame,text="Visa naturlig död statistik")
showNaturlig.pack(pady=12,padx=10)

root.mainloop()