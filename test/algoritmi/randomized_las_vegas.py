import random
from lp_solver import solve_lp_relaxation
from utils import *

def randomized_rounding_las_vegas(universo, F, seed=None):
    """
    Versione Las Vegas del Randomized Rounding.
    
    Ripete il rounding finché la cover è valida.
    Tempo: aleatorio (geometricamente distribuito)
    Correttezza: garantita
    
    Parametri
    ---------
    universo : set
    F        : list[set]
    seed     : seme per riproducibilità
    
    Ritorna
    -------
    (indici, n_iter) : cover valida e numero di iterazioni necessarie
    """
    rng = random.Random(seed)
    n = len(universo)

    # fase 1: LP — una volta sola
    x_hat = solve_lp_relaxation(universo, F)
    if x_hat is None:
        return None, -1

    # fase 2: rounding ripetuto fino al successo — nessun limite
    it = 0
    while True:
        it += 1
        selected = set()
        for j in range(len(F)):
            if rng.random() < x_hat[j]:
                selected.add(j)
        indici = sorted(selected)
        if is_valid_cover(universo, F, indici):
            return indici, it


def test1():

    X = {1, 2, 3, 4, 5}
    F = [{1,2,3}, {2,3,4}, {4,5}, {1,5}]
    indici, niter=randomized_rounding_las_vegas(X, F, seed=42)
    print(f"Universo: {X}")
    print(f"Famiglia di insiemi: {F}")
    print(f"Cover trovata: {indici}")
    print(f"N° iter: {niter}")

    assert is_valid_cover(X, F, indici), "La copertura trovata non è valida"

    return None

def test2():

    X2, F2 = generate_instance_bernoulli(n=10, m=5, p=0.4, seed=42)
    ind1, niter1= randomized_rounding_las_vegas(X2, F2, seed=99)
    ind2, niter2= randomized_rounding_las_vegas(X2, F2, seed=99)

    print(f"Universo: {X2}")
    print(f"Famiglia di insiemi: {F2}")
    print(f"Cover trovata con seed=99 (cov1): {ind1} (cov={len(ind1)} in N°iter={niter1})")
    print(f"Cover trovata con seed=99 (cov2): {ind2} (cov={len(ind2)} in N°iter={niter2})")

    assert is_valid_cover(X2, F2, ind1), "La copertura di Istanza 1 trovata non è valida"
    assert is_valid_cover(X2, F2, ind2), "La copertura di Istanza 2 trovata non è valida"

    assert ind1 == ind2, "stesso seed produce risultati diversi"
    assert niter1 == niter2, "stesso seed produce n° iter diversi"



    return None


def test3():

    X3, F3 = generate_worst_case(4)
    indici3, niter3= randomized_rounding_las_vegas(X3, F3, seed=42)
    print(f"Universo: {X3}")
    print(f"Famiglia di insiemi: {F3}")
    print(f"Cover trovata: {indici3}")
    print(f"N° iter: {niter3}")


    assert is_valid_cover(X3, F3, indici3), "La copertura trovata non è valida"


    return None

def test4():

    X, F = generate_instance_bernoulli(n=15, m=6, p=0.4, seed=42)
    successi = 0
    trials = 100
    for s in range(trials):
        indici, niter4 = randomized_rounding_las_vegas(X, F, seed=s)
        coperto = is_valid_cover(X, F, indici)
        if indici is not None and coperto:
            successi += 1
    tasso = successi / trials
    print(f"Copertura completa: {successi}/{trials} ({tasso:.1%})")
    print(f"N° iter: {niter4}")

    assert tasso >= 0.5, f"tasso di successo troppo basso: {tasso:.1%}"

    return None



def testRandomizedRoundingLasVegas():

    print("\nTest Randomized Rounding Set Cover - Las Vegas\n")

    print("CASO 1 - Istanza normale con universo di 5 elementi e 4 insiemi. Verifica che la copertura trovata sia valida.\n")
    test1()

    print("\nCASO 2 - Istanza generata casualmente con n=10, m=5, p=0.4 e seed=42. Verifica che la copertura trovata sia valida e che lo stesso seed produca risultati diversi.\n")
    test2()
    
    print("\nCASO 3 - Istanza worst-case per Greedy con k=4. Verifica che la copertura trovata sia valida.\n")
    test3()

    print("\nCASO 4 - Misura tasso di successi per 100 iter.\n")
    test4()


    return None

if __name__ == '__main__':
    
    testRandomizedRoundingLasVegas()