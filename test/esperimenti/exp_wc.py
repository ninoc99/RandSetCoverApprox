# Esperimento sulla risoluzione del WORST CASE (greedy fallisce).
import csv
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'algoritmi'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils import generate_instance_bernoulli, is_valid_cover
from brute_force import brute_force
from greedy import greedy_set_cover
from randomized import randomized_rounding
from ilp import ilp_set_cover
from utils import *

# parametri esperimento
k_val= [3,4,5,6,7,8]
fieldnames = ['k', 'n', 'algoritmo', 'dim_cover', 'opt', 'rho', 'valid']

# output CSV
output_path = os.path.join(os.path.dirname(__file__), 
              '..', 'risultati', 'exp_wc.csv')
os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for k in k_val:
        X, F = generate_worst_case(k)

        # calcola OPT con brute force
        _, opt = brute_force(X, F)
        
        # esegui ogni algoritmo e scrivi una riga
        for alg, func in [('Brute Force', brute_force),
                        ('ILP', ilp_set_cover),
                        ('Greedy', greedy_set_cover),
                        ('Randomized', randomized_rounding)]:
                try:
                    if alg == 'Greedy':
                        indici = func(X, F)
                        dim_cover = len(indici) if indici is not None else None
                    elif alg == 'Randomized':
                        indici = func(X, F, seed=42)
                        dim_cover = len(indici) if indici is not None else None
                    else:  # Brute Force e ILP
                        indici, dim_cover = func(X, F)
                
                    valid = is_valid_cover(X, F, indici) if indici is not None else False
                    rho = dim_cover / opt if (dim_cover is not None and opt > 0) else None
                except Exception as e:
                    print(f"Errore con {alg} (k={k}, n={len(X)}")
                
                    dim_cover, valid, rho = None, False, None
                writer.writerow({
                     'k': k,
                     'n': len(X),
                     'algoritmo': alg,
                     'dim_cover': dim_cover,
                     'opt': opt,
                     'rho': rho,
                     'valid': valid
                })
print(f"Esperimento completato. Risultati salvati in {output_path}")

