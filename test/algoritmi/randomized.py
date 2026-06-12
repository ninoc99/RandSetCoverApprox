import math
import random
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..')) # per importare utils (cartella superiore)
sys.path.append(os.path.dirname(__file__)) # per importare lp_solver (stesso livello)
from utils import generate_instance_bernoulli, generate_worst_case, is_valid_cover
from lp_solver import solve_lp_relaxation

def randomized_rounding(universo, F, c=2, seed=None):
    """
    Randomized rounding del rilassamento LP per Set Cover.
    
    Parametri
    ---------
    universo : set
    F        : list[set]
    c        : costante per t = ceil(c * ln(n)) round (in letteratura c=2 garantisce un tasso di successo pari al 99%)
    seed     : int | None
    
    Ritorna
    -------
    set[int] con gli indici degli insiemi selezionati, oppure None se il problema è infeasible.
    """
    rng = random.Random(seed)
    n = len(universo)
    t = math.ceil(c * math.log(n)) # numero di round di rounding
    
    # passo 1: risolvi il LP
    x_hat = solve_lp_relaxation(universo, F)
    if x_hat is None:
        return None
    
    # passo 2: t round di rounding randomizzato
    selected = set()
    for _ in range(t):
        for j in range(len(F)):
            if rng.random() < x_hat[j]:
                selected.add(j)
    
    return sorted(selected)


def test1():

    X = {1, 2, 3, 4, 5}
    F = [{1,2,3}, {2,3,4}, {4,5}, {1,5}]
    indici=randomized_rounding(X, F, seed=42)
    assert is_valid_cover(X, F, indici), "La copertura trovata non è valida"
    print(f"Universo: {X}")
    print(f"Famiglia di insiemi: {F}")
    print(f"Cover trovata: {indici}")

    return None

def test2():

    X2, F2 = generate_instance_bernoulli(n=10, m=5, p=0.4, seed=42)
    ind1 = randomized_rounding(X2, F2, seed=99)
    assert is_valid_cover(X2, F2, ind1), "La copertura trovata non è valida"
    ind2=randomized_rounding(X2, F2, seed=99)
    assert ind1 == ind2, "stesso seed produce risultati diversi"

    print(f"Universo: {X2}")
    print(f"Famiglia di insiemi: {F2}")
    print(f"Cover trovata con seed=99 (cov1): {ind1} (cov={len(ind1)})")
    print(f"Cover trovata con seed=99 (cov2): {ind2} (cov={len(ind2)})")

    return None


def test3():

    X3, F3 = generate_worst_case(4)
    indici3 = randomized_rounding(X3, F3, seed=42)
    assert is_valid_cover(X3, F3, indici3), "La copertura trovata non è valida"
    print(f"Universo: {X3}")
    print(f"Famiglia di insiemi: {F3}")
    print(f"Cover trovata: {indici3}")

    return None

def test4():

    X, F = generate_instance_bernoulli(n=15, m=6, p=0.4, seed=42)
    successi = 0
    trials = 100
    for s in range(trials):
        indici = randomized_rounding(X, F, seed=s)
        coperto = is_valid_cover(X, F, indici)
        if coperto:
            successi += 1
    tasso = successi / trials
    print(f"Copertura completa: {successi}/{trials} ({tasso:.1%})")
    assert tasso >= 0.5, f"tasso di successo troppo basso: {tasso:.1%}"

    return None



def testRandomizedRounding():

    print("\nTest Randomized Rounding Set Cover\n")

    print("CASO 1 - Istanza normale con universo di 5 elementi e 4 insiemi. Verifica che la copertura trovata sia valida.\n")
    test1()

    print("\nCASO 2 - Istanza generata casualmente con n=10, m=5, p=0.4 e seed=42. Verifica che la copertura trovata sia valida e che lo stesso seed produca risultati diversi.\n")
    test2()
    
    print("\nCASO 3 - Istanza worst-case per Greedy con k=4. Verifica che la copertura trovata sia valida.\n")
    test3()

    print("\nCASO 4 - Verifica che lo stesso seed produca risultati diversi.\n")
    test4()

    return None

if __name__ == '__main__':
    
    testRandomizedRounding()