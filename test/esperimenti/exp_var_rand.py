# Esperimento sulla variabilità del Randomized Rounding: su uno stesso input, quanto varia |C| tra esecuzioni con seed diversi?

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
n = 200
m = 50
p = 0.3
seeds_rand = list(range(200))
seed_istanza= 42


fieldnames = ['n', 'm', 'p', 'seed',
    'algoritmo', 'dim_cover', 'valid']

# output CSV
output_path = os.path.join(os.path.dirname(__file__), 
              '..', 'risultati', 'exp4_var_rand.csv')
os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    X,F=generate_instance_bernoulli(n,m,p,seed_istanza)

    # esegui ogni algoritmo e scrivi una riga
    for alg, func in [('Greedy', greedy_set_cover),
                    ('Randomized', randomized_rounding)]:
            
            for seed in seeds_rand:
                try:
                    if alg == 'Greedy':
                        indici = func(X, F)
                        dim_cover = len(indici) if indici is not None else None
                    elif alg == 'Randomized':
                        indici = func(X, F, seed=seed)
                        dim_cover = len(indici) if indici is not None else None
                    else:
                        None
        
                    valid = is_valid_cover(X, F, indici) if indici is not None else False
                except Exception as e:
                    print(f"Errore con {alg} (n={n}, m={m}, p={p}, seed={seed}): {e}")
                
                    dim_cover, valid = None, False
                writer.writerow({
                    'n': n,
                    'm': m,
                    'p': p,
                    'seed': seed,
                    'algoritmo': alg,
                    'dim_cover': dim_cover,
                    'valid': valid
                })
print(f"Esperimento completato. Risultati salvati in {output_path}")

