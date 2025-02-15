
import test

from pylak import MazeGame

# Lav et spil med en karakter Kurt som er i en labyrint
game = MazeGame(True)

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



# Få programmet til at køre 🛫🛫🛫
game.start(program)