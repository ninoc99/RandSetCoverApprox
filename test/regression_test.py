# Area di test per gli algoritmi implementati. Qui puoi eseguire test di regressione, confrontare soluzioni, ecc.
# Puoi eseguire questo script per verificare che tutte le implementazioni funzionino correttamente su istanze specifiche, 
# come quella worst-case per il Greedy.


import sys
import os
sys.path.append(os.path.dirname(__file__)) # per importare utils (stesso livello)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'algoritmi'))

import sys
import os
sys.path.append(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'algoritmi'))

from brute_force import testBruteForce
from greedy import testGreedy
from greedy_hash_pattern import testGreedyHashMap
from ilp import testILP
from randomized import testRandomizedRounding
from randomized_las_vegas import testRandomizedRoundingLasVegas
from utils import testIstanceGenerators



if __name__ == '__main__':


    #GENERATORI DI ISTANZE
   
    # Test di validità su generatori di istanze
    testIstanceGenerators()

    #--------------------------------------------------#

    #ALGORITMI IMPLEMENTATI PER IL PROBLEMA DI SET COVER
    
    ## Algoritmi esatti
    ### 1) BRUTE FORCE
    testBruteForce()

    ### 2) ILP
    testILP()

    ## Algoritmi di approssimazione
    ### 3) GREEDY
    testGreedy()

    ### 4) RANDOMIZED ROUNDING - Monte Carlo
    testRandomizedRounding()
    
    ### 5) RANDOMIZED ROUNDING - Las Vegas
    testRandomizedRoundingLasVegas()

    ### 6) GREEDY - PATTERN HASH MAP
    testGreedyHashMap()