import random as _rnd
import statistics as _stats

def generate_instance_bernoulli(n, m, p, seed=None):
    """
    Genera un'istanza casuale con n e m fissi e copertura garantita.
    Ogni elemento è incluso in ogni insieme con probabilità p (Bernoulli).
    Se un elemento non viene incluso in nessun insieme, viene assegnato a uno scelto casualmente.

    Parametri
    ---------
    n       : dimensione dell'universo
    m       : numero di insiemi (fisso)
    p       : probabilità di inclusione di ogni elemento in ogni insieme (0 < p < 1)
    seed    : int | None
    """
    
    rng = _rnd.Random(seed)
    universo = set(range(1, n + 1))
    
    F = []
    
    for _ in range(m):
        S = {el for el in universo if rng.random() < p}
        if not S:
            S.add(rng.choice(list(universo)))  # almeno un elemento
        F.append(S)

    # distribuisce gli elementi scoperti negli insiemi esistenti
    uncovered = list(universo - set().union(*F))
    for el in uncovered:
        rng.choice(F).add(el)

    return universo, F

def is_valid_cover(X, F, cover):
    """
    Verifica che la cover selezionata copra tutto l'universo.
    X: universo
    F: famiglia di insiemi
    cover: lista di indici 0-based degli insiemi scelti
    """
    covered = set()
    for idx in cover:
        covered.update(F[idx])
    return covered == X

def generate_worst_case(k):
    """
    Genera l'istanza worst-case per il Greedy (Feige 1998).
    k >= 3 — ottimo = 2, Greedy deterministico trova k insiemi.
    n = 2^(k+1) - 2 elementi, m = k+2 insiemi.
    """
    s_sets, cur = [], 1
    for i in range(1, k + 1):
        s = set(range(cur, cur + 2**i))
        s_sets.append(s)
        cur += 2**i
    universe = set(range(1, cur))
    t1, t2 = set(), set()
    for s in s_sets:
        elems = sorted(s)
        mid = len(elems) // 2
        t1.update(elems[:mid])
        t2.update(elems[mid:])
    return universe, s_sets + [t1, t2]


def test1(n,m,p):

    X, F = generate_instance_bernoulli(n, m, p, seed=42)
    print("X =", X)
    print("F =", F)
    # universo corretto
    assert len(X) == n, f"atteso n={n}, ottenuto {len(X)}"  
    # numero di insiemi corretto
    assert len(F) == m, f"atteso m={m}, ottenuto {len(F)}"
    # copertura garantita con p=0.0
    assert (set().union(*F) == X), "Copertura non garantita con p=0.0"
    # ogni insieme contiene esattamente un elemento
    assert all(len(S) >= 1 for S in F), "Nessun insieme dovrebbe essere vuoto"

    return None

def test2(n,m):
    
    plist=[0.1, 0.3, 0.5, 0.7, 0.9]
    for p in plist:
        X2, F2 = generate_instance_bernoulli(n, m, p=p, seed=123)
        sizes = [len(S) for S in F2]
        assert set().union(*F2) == X2, f"copertura non garantita con p={p}"
        assert all(len(S) >= 1 for S in F2), f"insieme vuoto con p={p}"
        print(f"p={p:.1f} | media={_stats.mean(sizes):.1f} "
            f"| min={min(sizes)} | max={max(sizes)}")

    return None

def test3(n,m):

    seed=[42, 7, 1, 123]
    for s in seed:
        X3, F3 = generate_instance_bernoulli(n, m, p=0.5, seed=s)
        sizes = [len(S) for S in F3]
        assert set().union(*F3) == X3, f"copertura non garantita con seed={s}"
        assert all(len(S) >= 1 for S in F3), f"insieme vuoto con seed={s}"
        print(f"seed={s} | media={_stats.mean(sizes):.1f} "
            f"| min={min(sizes)} | max={max(sizes)}")
        
    return None

def test4(n, m, p):

    X_a, F_a = generate_instance_bernoulli(n, m, p, seed=42)
    X_b, F_b = generate_instance_bernoulli(n, m, p, seed=42)
    print("Istanza A:", X_a, F_a)
    print("Istanza B:", X_b, F_b)
    assert X_a == X_b, "stesso seed produce universi diversi"
    assert F_a == F_b, "stesso seed produce famiglie diverse"

    return None


def testIstanceGenerators():

    n=10
    m=4
    p=0.0

    print("\nTest Generatori di istanze\n")

    print("\nTEST 1 - Istanza con p=0.0 (nessun elemento incluso casualmente, ma copertura garantita)\n")
    test1(n, m, p)

    print("\nTEST 2 - Variazione di p con n=10, m=4 e seed=123. Come la scelta di p influenza la dimensione media degli insiemi.\n")
    test2(n, m)

    print("\nTEST 3 - Variazione del seed con n=10, m=4, p=0.5. Come la scelta del seed influenza la dimensione media degli insiemi.\n")
    test3(n, m)

    print("\nTEST 4 - Verifica che lo stesso seed produce la stessa istanza (universo e famiglia di insiemi).\n")
    test4(n, m, p=0.5)


    return None


if __name__ == '__main__':

    testIstanceGenerators()
