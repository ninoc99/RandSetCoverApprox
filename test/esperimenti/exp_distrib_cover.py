#Esperimento su come si distribuisce la soluzione di Randomized Rounding - n variabile

import csv
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'algoritmi'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils import generate_instance_bernoulli, is_valid_cover
from greedy import greedy_set_cover
from randomized import randomized_rounding
from ilp import ilp_set_cover
from utils import *

# parametri esperimento
n_val= [20, 40, 80, 160, 320]
m = 50
p = 0.3
seeds_rand = list(range(500))
seed_istanza= 42


fieldnames = ['n', 'm', 'p', 'seed', 'dim_cover', 'valid']

# output CSV
output_path = os.path.join(os.path.dirname(__file__), 
              '..', 'risultati', 'exp7_distrib_cover.csv')
os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for n in n_val:
        X,F=generate_instance_bernoulli(n,m,p,seed_istanza)
        
        for s in seeds_rand:
            try:
                indici = randomized_rounding(X, F, seed=s)
                dim_cover = len(indici) if indici is not None else None
                valid = is_valid_cover(X, F, indici) if indici is not None else False
            except Exception as e:
                print(f"Errore con Randomized Rounding Alg. (n={n}, m={m}, p={p}, seed={s}): {e}")
                dim_cover, valid = None, False

            writer.writerow({
                'n': n,
                'm': m,
                'p': p,
                'seed': s,
                'dim_cover': dim_cover,
                'valid': valid
            })
print(f"Esperimento completato. Risultati salvati in {output_path}")

