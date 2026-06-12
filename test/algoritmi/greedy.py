import math
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils import generate_instance_bernoulli, generate_worst_case, is_valid_cover
from brute_force import brute_force 

# ─────────────────────────────────────────────────────────────
# GREEDY
# ─────────────────────────────────────────────────────────────

def greedy_set_cover(universo, F):
    """
    Ad ogni passo seleziona l'insieme che copre il maggior numero di elementi rimanenti.
    Complessità: O(m * n) per ogni iterazione, fino a coprire tutto l'universo.
    Approssimazione: H(max|S|) ≤ ln(n) + 1

    Parametri
    ---------
    universo : set
    F        : list[set]

    Ritorna
    -------
    list[set] con gli insiemi selezionati, oppure None se non esiste soluzione.
    """
    covered = set()
    selected_indices = []

    while covered != universo:
        best_idx = None
        best_cover = 0
        for i, subset in enumerate(F):
            cover_size = len(subset - covered)
            if cover_size > best_cover:
                best_cover = cover_size
                best_idx = i
        if best_idx is None:
            return None  # Universo non copribile
        selected_indices.append(best_idx)
        covered.update(F[best_idx])

    return selected_indices


def test1():

    X = {1, 2, 3, 4, 5}
    F = [{1,2,3}, {2,3,4}, {4,5}, {1,5}]
    
    print("Universo:", X)
    print("Famiglia di insiemi:", F)
    indici = greedy_set_cover(X, F)
    
    assert is_valid_cover(X, F, indici), "La copertura trovata non è valida"
    print(f"Esito test 1 - Cover trovata: {indici}")

    return None

def test2():

    X2 = {1, 2, 3}
    F2 = [{1,2,3}, {1,2}, {3}]
    indici2 = greedy_set_cover(X2, F2)
    assert is_valid_cover(X2, F2, indici2), "La copertura trovata non è valida"
    print(f"Esito test 2 - Cover trovata: {indici2}")

    return None

def test3():

    X3, F3 = generate_instance_bernoulli(n=10, m=5, p=0.4, seed=42)
    indici3 = greedy_set_cover(X3, F3)
    assert is_valid_cover(X3, F3, indici3), "La copertura trovata non è valida"
    print(f"Universo: {X3}")
    print(f"Famiglia di insiemi: {F3}")
    print(f"Esito test 3 - Cover trovata: {indici3}")

    return None

def test4():

    X4,F4=generate_instance_bernoulli(n=20, m=8, p=0.5, seed=42)
    indici4 = greedy_set_cover(X4, F4)

    assert is_valid_cover(X4, F4, indici4), "cover greedy non valida"

    # bound di approssimazione: mai peggio di H(max|S|) * OPT
    _, opt = brute_force(X4, F4)
    max_size = max(len(S) for S in F4)
    H = sum(1/i for i in range(1, max_size+1))
    assert len(indici4) <= H * opt + 1, "greedy supera il bound teorico"


    assert is_valid_cover(X4, F4, indici4), "La copertura trovata non è valida"
    print(f"Universo: {X4}")
    print(f"Famiglia di insiemi: {F4}")
    print(f"Esito test 4 - Cover trovata: {indici4}")
    print(f"Bound teorico: H({max_size}) * OPT = {H:.4f} * {opt} = {H * opt:.4f}")
    print(f"Greedy trova: {len(indici4)} insiemi — rispetta il bound: {len(indici4) <= H * opt + 1}")

    return None

def test5():
    
    k=4

    X5, F5 = generate_worst_case(k)
    indici5 = greedy_set_cover(X5, F5)
    assert is_valid_cover(X5, F5, indici5), "La copertura trovata non è valida"

    _, opt = brute_force(X5, F5)
    max_size = max(len(S) for S in F5)
    H = sum(1/i for i in range(1, max_size+1))
    assert len(indici5) <= H * opt + 1, "greedy supera il bound teorico"

    print(f"Universo: {X5}")
    print(f"Famiglia di insiemi: {F5}")
    print(f"Esito test 5 - Cover trovata: {indici5} (ottimo è 2, greedy trova {len(indici5)})")

    print(f"Bound teorico: H({max_size}) * OPT = {H:.4f} * {opt} = {H * opt:.4f}")
    print(f"Greedy trova: {len(indici5)} insiemi")
    print(f"Rapporto empirico: {len(indici5)/opt:.4f} (bound teorico: {H:.4f})")

    return None


def testGreedy():

    print("\nTest Greedy Set Cover\n")

    print("\nTEST 1 - Istanza normale con universo di 5 elementi e 4 insiemi. Ottimo è 2.\n")
    test1()

    print("\nTEST 2 - Istanza con universo di 3 elementi e 3 insiemi, dove uno copre tutto. Ottimo è 1.\n")
    test2()

    print("\nTEST 3 - Istanza generata casualmente con universo di 10 elementi e 5 insiemi.\n")
    test3()

    print("\nTEST 4 - Istanza generata casualmente con universo di 20 elementi e 8 insiemi. Verifica che la copertura trovata sia valida e rispetti il bound di approssimazione.\n")
    test4()

    print("\nTEST 5 - Istanza worst-case per Greedy con k=4. Ottimo è 2, ma greedy potrebbe trovare una cover di dimensione k.\n")
    test5()


    return None


if __name__ == '__main__':

    testGreedy()