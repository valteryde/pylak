

import test

from pylak import MazeGame

import time

# Lav et spil med en karakter Kurt som er i en labyrint
# game = MazeGame(False, size=19, timePerMove=0.1)
game = MazeGame(True, size=5, timePerMove=1)

controls = game.controls() # bruges til at styre kurt
sensor = game.sensor() # bruges til at tjekke om der er vægge hvor vi kigger hen
memory = game.memory() # bruges til at tjekke om vi har været et sted før
goal = game.goal() # bruges til at tjekke om vi er nået i mål
back = game.back() # bruges til at gå tilbage (hvis vi nu er gået forkert)


def program():
    
    # flood fill med en stack
    directions = [(-1,0),(1,0),(0,1),(0,-1)]

    while True:
    
        x, y = game.pos

        if goal():
            return

        openWalls = sensor()

        for i, wall in enumerate(openWalls):

            if wall:

                # måske lav en funktion som tjekker om de har været der
                dx, dy = directions[i]
                if memory(x+dx, y+dy):
                    continue
                
                controls[i]()

                break
        
        else:
            
            # backtrack
            back()


game.start(program)
