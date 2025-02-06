
# ide:
# lav et mini spil hvor man kan samle noget op og ligge det ned
# 2-link robot
# måske sensor
# elev kan programmere retninger og så kan de ved funktioner og loops forbedre det.
# så kan der indsættes en væg som de skal styre udenom

import test

from pylak import Engine, RobotSimulation, RobotArm

# Min robot hedder Kurt 🤩🤖💃 (min robot er en arm)
kurt = RobotArm()

# Vi skal styre Kurt. Det gør vi i et program 💪🧑‍💻
def program():
    
    # få kurt til at bevæge sig 🏃
    # kurt.moveLeft(v=10)
    kurt.setDestination([200, 200])

    yield # vi bruger "yield" til at vente på at kurt bevæger sig ⏰
    # Hvis vi ikke venter på at Kurt bliver færdig så bliver kurt helt forvirret

    # få kurt til at bevæge sig til venstre
    print('hejsa')
    kurt.setDestination([400, 250])

    yield # vi venter igen

    print('Vi er færdig!')


# Få robotsimulationen til at køre 🛫🛫🛫
sim = RobotSimulation( program, kurt)
sim.start()