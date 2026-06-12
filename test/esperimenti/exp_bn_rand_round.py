import time
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..')) # per importare utils (cartella superiore)
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'algoritmi'))

BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
DATA_DIR = os.path.join(BASE_DIR, "risultati")


from utils import generate_instance_bernoulli, generate_worst_case, is_valid_cover
from lp_solver import solve_lp_relaxation
import random
import time
import math
import csv
import pandas as pd

def randomized_rounding(universo, F, c=2, seed=None, return_times=False):
    
    rng = random.Random(seed)
    n = len(universo)
    t = math.ceil(c * math.log(n))
    
    # fase 1: LP
    t0 = time.perf_counter()
    x_hat = solve_lp_relaxation(universo, F)
    t_lp = time.perf_counter() - t0
    if x_hat is None:
        return None

    # fase 2: rounding
    t0 = time.perf_counter()
    selected = set()
    for _ in range(t):
        for j in range(len(F)):
            if rng.random() < x_hat[j]:
                selected.add(j)
    t_round = time.perf_counter() - t0

    # fase 3: verifica
    t0 = time.perf_counter()
    indici = sorted(selected)
    t_verifica = time.perf_counter() - t0

    if return_times:
        return indici, {'t_lp': t_lp, 't_round': t_round, 't_verifica': t_verifica}
    return indici

def expBottleneckRoundRand():

    #Esperimenti sull'andamento temporale dell'Algoritmo Greedy e Randomized Rounding.

    # parametri esperimento
    n_vals  = [50, 100, 200, 400, 800]
    m_vals  = [20, 50, 100]
    p  = 0.3
    seeds   = [42, 123, 7, 31, 999]

    fieldnames = ['n', 'm', 'p', 'seed',
                't_lp', 't_round', 't_verifica', 't_totale']

    # output CSV
    output_path = os.path.join(os.path.dirname(__file__), 
                '..', 'risultati', 'exp9_bottleneckRoundRand.csv')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for n in n_vals:
            for m in m_vals:
                for seed in seeds:
                    X, F = generate_instance_bernoulli(n, m, p, seed)
                    try:
                        _,tempi=randomized_rounding(X,F, seed=seed, return_times=True)
                        t_totale=tempi['t_lp'] + tempi['t_round'] + tempi['t_verifica']
                    except Exception as e:
                        print(f"Errore con Randomized Rounding Alg: (n={n}, m={m}, p={p}, seed={seed}): {e}")

                    writer.writerow({
                        'n': n,
                        'm': m,
                        'p': p,
                        'seed': seed,
                        't_lp':tempi['t_lp'],
                        't_round':tempi['t_round'],
                        't_verifica':tempi['t_verifica'],
                        't_totale':t_totale
                    })

    print(f"Esperimento completato. Risultati salvati in {output_path}")

    return None

def analisiBottleneck():

    df = pd.read_csv(os.path.join(DATA_DIR, 'exp9_bottleneckRoundRand.csv'))

    print("\nANALISI BOTTLENECK RANDOMIZED ROUNDING\n")

    # percentuale di tempo per fase, media su tutti i trial
    df['pct_lp']       = df['t_lp']       / df['t_totale'] * 100
    df['pct_round']    = df['t_round']     / df['t_totale'] * 100
    df['pct_verifica'] = df['t_verifica']  / df['t_totale'] * 100

    print("Percentuale media per fase:")
    print(f"  LP:       {df['pct_lp'].mean():.1f}%")
    print(f"  Rounding: {df['pct_round'].mean():.1f}%")
    print(f"  Verifica: {df['pct_verifica'].mean():.1f}%")

    # tempo medio per fase e n
    print("\nTempo medio per fase e n:")
    summary = df.groupby('n')[['t_lp','t_round','t_verifica']].mean()
    print(summary.to_string())

    # tempo medio per fase e m
    print("\nTempo medio per fase e m:")
    summary_m = df.groupby('m')[['t_lp','t_round','t_verifica']].mean()
    print(summary_m.to_string())

    return None

if __name__ == '__main__':
    expBottleneckRoundRand()
    analisiBottleneck()



