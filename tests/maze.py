
# ide:
# lav et mini spil hvor man kan samle noget op og ligge det ned
# 2-link robot
# måske sensor
# elev kan programmere retninger og så kan de ved funktioner og loops forbedre det.
# så kan der indsættes en væg som de skal styre udenom

# IKKE ROBOT 
# Men måske bare et farmer spil? ligesom harvest
# Navigations spil

import test

from pylak import MazeGame

# Lav et spil med en karakter Kurt som er i en labyrint
game = MazeGame()

# Få fire funktioner så vi kan styre Kurt
left, right, up, down = game.controls()

# Vi skal styre en lille karakter Kurt
# Det gør vi i et program 🧑‍💻👣
def program():
    
    # få kurt til at bevæge sig 🏃
    right()

    # få kurt til at bevæge sig til højre
    right()

    # få kurt til at bevæge sig nedad
    down()


# Få robotsimulationen til at køre 🛫🛫🛫
game.start(program)