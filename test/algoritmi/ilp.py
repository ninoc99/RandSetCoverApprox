import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils import generate_instance_bernoulli, generate_worst_case, is_valid_cover 
from brute_force import brute_force

# ─────────────────────────────────────────────────────────────
# ILP  (Gurobi)
# ─────────────────────────────────────────────────────────────

def ilp_set_cover(universo, F, time_limit=None, lp_path=None, label=None):
    """
    Soluzione ottima tramite Programmazione Lineare Intera (Gurobi).

    Formulazione:
        min  Σ_j x_j
        s.t. Σ_{j : e ∈ S_j} x_j ≥ 1   ∀ e ∈ X
             x_j ∈ {0, 1}

    Parametri
    ---------
    universo   : set
    F          : list[set]
    time_limit : float | None — limite in secondi (None = nessun limite)
    lp_path    : str | None   — percorso esplicito del file .lp; sovrascrive label
    label      : str | None   — nome logico del contesto chiamante (es. "validity",
                               "stress", "density"); produce logs/set_cover_{label}.lp.
                               Se None usa logs/set_cover.lp

    Ritorna
    -------
    (list[int], int) con gli indici 0-based degli insiemi selezionati e il valore ottimo,
    oppure (None, None) se Gurobi non è disponibile o il modello è infeasible.
    """
    try:
        import gurobipy as gp
        from gurobipy import GRB
    except ImportError:
        print("[WARN] Gurobi non disponibile — ILP saltato.")
        return None, None

    import os as _os
    if lp_path is None:
        _logs_dir = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..", "logs")
        _os.makedirs(_logs_dir, exist_ok=True)
        _name = f"set_cover_{label}.lp" if label else "set_cover.lp"
        lp_path = _os.path.join(_logs_dir, _name)

    sets = [set(s) for s in F]
    m = len(sets)
    elements = list(universo)

    env = gp.Env(empty=True)
    env.setParam("OutputFlag", 0)
    env.start()
    model = gp.Model(env=env, name="SetCover")
    if time_limit is not None:
        model.setParam("TimeLimit", time_limit)

    x = model.addVars(m, vtype=GRB.BINARY, name="x")
    model.setObjective(gp.quicksum(x[j] for j in range(m)), GRB.MINIMIZE)

    for e in elements:
        covering = [j for j in range(m) if e in sets[j]]
        if covering:
            model.addConstr(
                gp.quicksum(x[j] for j in covering) >= 1,
                name=f"cover_{e}"
            )

    model.write(lp_path)

    model.optimize()

    if model.Status in (GRB.OPTIMAL, GRB.TIME_LIMIT) and model.SolCount > 0:
        selected = [j for j in range(m) if x[j].X > 0.5]
        return selected, int(round(model.ObjVal))

    return None, None

def test1():

    X = {1, 2, 3, 4, 5}
    F = [{1,2,3}, {2,3,4}, {4,5}, {1,5}]
    indici, size = ilp_set_cover(X, F)

    _, opt_bf = brute_force(X, F)

    assert is_valid_cover(X, F, indici), "La copertura trovata non è valida"
    assert size == opt_bf, f"ILP={size} != BF={opt_bf}"

    print(f"Esito caso 1 - Cover trovata: {indici} con dimensione {size}")

    return None

def test2():

    X2, F2 = generate_instance_bernoulli(n=10, m=5, p=0.4, seed=42)
    indici2, size2 = ilp_set_cover(X2, F2)

    _, opt_bf = brute_force(X2, F2)

    assert is_valid_cover(X2, F2, indici2), "La copertura trovata non è valida"
    assert size2 == opt_bf, f"ILP={size2} != BF={opt_bf}"

    print(f"Universo: {X2}")
    print(f"Famiglia di insiemi: {F2}")
    print(f"Esito caso 2 - Cover trovata: {indici2} con dimensione {size2}")

    return None

def test3():

    X3, F3 = generate_worst_case(4)
    indici3, size3 = ilp_set_cover(X3, F3)
    assert is_valid_cover(X3, F3, indici3), "La copertura trovata non è valida"
    print(f"Esito caso 3 - Cover trovata: {indici3} con dimensione {size3} (ottimo = 2)")


def testILP():

    print("\nTest ILP Set Cover\n")

    print("CASO 1 - Istanza normale con universo di 5 elementi e 4 insiemi. Verifica che la copertura trovata sia valida e ottima.\n")
    test1()

    print("\nCASO 2 - Istanza generata casualmente con n=10, m=5, p=0.4 e seed=42. Verifica che la copertura trovata sia valida.\n")
    test2()

    print("\nCASO 3 - Istanza worst-case per Greedy con k=4. Verifica che la copertura trovata sia valida e ottima (dimensione 2).\n")
    test3()
    
    return None



if __name__ == '__main__':

    testILP()