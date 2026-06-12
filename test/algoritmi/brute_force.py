import itertools
import random
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils import * 

# ─────────────────────────────────────────────────────────────
# BRUTE FORCE
# ─────────────────────────────────────────────────────────────

def brute_force(universo, F):
    """
    Esplora tutte le combinazioni di sottoinsiemi per trovare la copertura minima.
    Complessità: O(2^m * n)

    Parametri
    ---------
    universo : set
    F        : list[set]

    Ritorna
    -------
    (combinazione, dimensione) oppure None se non esiste soluzione.
    """
    for i in range(1, len(F) + 1):
        for combination in itertools.combinations(range(len(F)), i):
            union_set = set()
            for idx in combination:
                union_set = union_set.union(F[idx])
            if universo.issubset(union_set):
                return list(combination), i
    return None, None

def test1():
   
    X = {1, 2, 3, 4, 5}
    F = [{1,2,3}, {2,3,4}, {4,5}, {1,5}]

    print("Universo:", X)
    print("Famiglia di insiemi:", F)

    indici, size = brute_force(X, F)
    assert size == 2, f"atteso OPT=2, ottenuto {size}"
    assert is_valid_cover(X, F, indici), "cover non valida"

    print(f"Esito test 1 - Cover trovata: insiemi {indici} con dimensione {size}")

    return None

def test2():

    X2 = {1, 2, 3}
    F2 = [{1,2,3}, {1,2}, {3}]

    print("Universo:", X2)
    print("Famiglia di insiemi:", F2)

    indici2, size2 = brute_force(X2, F2)
    assert size2 == 1, f"atteso OPT=1, ottenuto {size2}"
    assert is_valid_cover(X2, F2, indici2), "La copertura trovata non è valida"

    print(f"Esito test 2 - Cover trovata: insiemi {indici2} con dimensione {size2}")

    return None

def test3():

    X3, F3 = generate_instance_bernoulli(n=10, m=5, p=0.4, seed=42)
    indici3, size3 = brute_force(X3, F3)
    assert is_valid_cover(X3, F3, indici3), "La copertura trovata non è valida"
    print(f"Universo: {X3}")
    print(f"Famiglia di insiemi: {F3}")
    print(f"Esito test 3 - Cover trovata: insiemi {indici3} con dimensione {size3}")

    return None

def test4():
    
    k=4

    X4, F4 = generate_worst_case(k)
    indici4, size4 = brute_force(X4, F4)
    assert is_valid_cover(X4, F4, indici4), "La copertura trovata non è valida"
    assert size4 == 2, f"atteso OPT=2, ottenuto {size4}"

    print(f"Universo: {X4}")
    print(f"Famiglia di insiemi: {F4}")
    print(f"Esito test 4 - Cover trovata: insiemi {indici4} con dimensione {size4}")

    return None



def testBruteForce():

    print("\nTest Brute Force Set Cover\n")

    print("\nTEST 1 - Istanza normale con universo di 5 elementi e 4 insiemi. Ottimo è 2.\n")
    test1()
    print("\nTEST 2 - Istanza con universo di 3 elementi e 3 insiemi, dove uno copre tutto. Ottimo è 1.\n")
    test2()
    print("\nTEST 3 - Istanza generata casualmente con n=10, m=5, p=0.4 e seed=42. Verifica che la copertura trovata sia valida.\n")
    test3()
    print("\nTEST 4 - Istanza worst-case per Greedy con n=4. Ottimo è 2.\n")
    test4()

    return None


if __name__ == '__main__':

    testBruteForce()