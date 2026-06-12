import pulp
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils import generate_instance_bernoulli, generate_worst_case, is_valid_cover

def solve_lp_relaxation(universo, F):
    """
    Risolve il rilassamento LP del Set Cover.
    Ritorna il vettore x_hat con x_hat[j] in [0,1] per ogni insieme j.
    
    Parametri
    ---------
    universo : set
    F        : list[set]
    
    Ritorna
    -------
    list[float] — valore frazionario x_hat[j] per ogni j,
    oppure None se il problema è infeasible.
    """
    m = len(F)
    
    # crea il problema di minimizzazione
    prob = pulp.LpProblem("SetCover_LP", pulp.LpMinimize)
    
    # variabili: x[j] in [0,1] per ogni insieme j
    x = [pulp.LpVariable(f"x_{j}", lowBound=0, upBound=1) 
         for j in range(m)]
    
    # obiettivo: min sum x[j]
    prob += pulp.lpSum(x)
    
    # vincoli: per ogni elemento e, sum_{j: e in F[j]} x[j] >= 1
    for e in universo:
        covering = [x[j] for j in range(m) if e in F[j]]
        if covering:
            prob += pulp.lpSum(covering) >= 1
    
    # risolvi silenziosamente
    prob.solve(pulp.PULP_CBC_CMD(msg=0))
    
    if pulp.LpStatus[prob.status] == "Optimal":
        return [pulp.value(x[j]) for j in range(m)]
    return None


if __name__ == '__main__':
    X = {1, 2, 3, 4, 5}
    F = [{1,2,3}, {2,3,4}, {4,5}, {1,5}]

    x_hat = solve_lp_relaxation(X, F)
    print("Soluzione LP:")
    for j, val in enumerate(x_hat):
        print(f"  x[{j}] = {val:.4f}  (insieme {F[j]})")
    print(f"OPT_LP = {sum(x_hat):.4f}")

    X4, F4 = generate_worst_case(4)
    x_hat4 = solve_lp_relaxation(X4, F4)
    print("Soluzione LP worst-case:")
    for j, val in enumerate(x_hat4):
        print(f"  x[{j}] = {val:.4f}  (|S|={len(F4[j])})")
    print(f"OPT_LP = {sum(x_hat4):.4f}")