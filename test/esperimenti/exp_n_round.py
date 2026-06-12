#Studio di come il n° di round (t=c*ln(n)) del Randomized Alg. influenza la qualità della soluzione. 
# Trade off: c piccolo: pochi round, soluzione più compatta ma prob. di fallimento maggiore. c grande: tanti round, copertura quasi certamente completa ma soluzione più grande.

import csv
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'algoritmi'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils import generate_instance_bernoulli, is_valid_cover
from randomized import randomized_rounding
from utils import *
import math

# parametri esperimento
n = 50
m = 20
p = 0.3
seeds_rand = list(range(200))
seed_istanza= 42
c_vals = [1,2,3,4]

fieldnames = [
            'n', 'm', 'p', 'seed', 'c', 't',
            'dim_cover', 'valid']

# output CSV
output_path = os.path.join(os.path.dirname(__file__), 
              '..', 'risultati', 'exp5_n_round.csv')
os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    X,F=generate_instance_bernoulli(n,m,p,seed_istanza)

    for c in c_vals:
        t=math.ceil(c*math.log(n)) #t=round per eccesso di c*log(n)
        for seed in seeds_rand:
            try:
                indici = randomized_rounding(X, F, c=c, seed=seed)
                dim_cover = len(indici) if indici is not None else None
                valid = is_valid_cover(X, F, indici) if indici is not None else False
            except Exception as e:
                print(f"Errore con Randomized (n={n}, m={m}, p={p}, seed={seed}, c={c}, t={t}): {e}")
            
                dim_cover, valid = None, False
            writer.writerow({
                'n': n,
                'm': m,
                'p': p,
                'seed': seed,
                'c': c,
                't': t,
                'dim_cover': dim_cover,
                'valid': valid
            })
print(f"Esperimento completato. Risultati salvati in {output_path}")
