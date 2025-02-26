
"""
Hejsa!

Mål for denne øvelse er at lave en *mekansime* i et 2D spil

Der er mange forskellige mekanismer det kunne være:
* Snakke med en NPC
* Samle en genstand op
* Skifte rum
* Åbne en dør
* Lave en fælde
* Få en fjende til at jagte en

I skal vælge en mekanisme og implementere den i et 2D spil.
Mekansimen skal være simpel og ikke for kompleks (svær). 
*Husk at en god kodebase er en simpel kodebase*

Jeg forslår i starter med at lave en simpel mekanisme, som at samle en genstand op.

Preskrevet kode:
* pylak
* scene
* spiller

I skal skrive
* Mekansimen

"""

import test # slet den her linje

from pylak import Engine, ControllablePlayer, Rectangle, Circle

# Vi laver her vores engine
engine = Engine()

# Her er det i skal ændre på. Det her objekt
# kan være en genstand som spilleren kan samle op, en fjende som spilleren kan slå ihjel, 
# en dør som spilleren kan åbne. Altså alt muligt. Den vil være jeres *mekansime*
class MinMekanisme:
    
    # Husk at __init__ er spawner metoden (det vil sige at den køres når objektet bliver spawnet)
    # Den køres når man skriver MinMekanisme()´
    def __init__(self):
        
        # Jeg har givet den en x og y værdi. 
        # TODO: Hvad sker der hvis man ændrer 0 til 200?
        self.x = 0
        self.y = 0

        # Hvordan skal den se ud på skærmen?
        # Det kan vi fikse med en Firkant (Rectangle)
        # TODO: Hvad sker der når vi ændrer 50 til 100
        self.rect = Rectangle(50, 50)


    def update(self):
        # TODO: Skal mekanismen gøre noget? altså skal den opdateres
        pass

    
    def draw(self):
        # TODO: Skal mekanismen tegnes på skærmen?
        # Lige nu bruger vi bare den firkant vi lavede i __init__
        # Så vi tegner firkanten på skærmen her
        self.rect.draw(self.x, self.y)


# Scene (også kaldet et gameloop)
class Scene:

    def setup(self):
        # I scenen gemmer vi vores spiller
        self.player = ControllablePlayer(engine)

        # Og vi gemmer vores mekanisme
        # HUSK at ændre dette objekt til jeres mekanisme
        self.mechanism = MinMekanisme() # Her kører __init__ metoden (funktionen)


    def update(self, dt):
        
        # Vi opdaterer spilleren så den bevæger sig rundt
        self.player.update() #TODO: Prøv at udkommenter dette

        # Og vi opdaterer mekanismen
        self.mechanism.update() # Her kører vi update metoden (funktionen)


    def draw(self):
        
        # Vi tegner her spilleren
        self.player.draw()
        
        # Og vi tegner mekanismen
        self.mechanism.draw() # Her kører vi draw metoden (funktionen)



# start game loopet
scene = Scene()
engine.setCurrentScene(scene)
engine.start()