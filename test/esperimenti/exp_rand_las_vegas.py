#Confronto tra Randomized Rounding Las Vegas vs Monte Carlo.

import csv
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'algoritmi'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils import generate_instance_bernoulli, is_valid_cover
from randomized import randomized_rounding
from randomized_las_vegas import randomized_rounding_las_vegas
from utils import *
import math


# parametri esperimento
n_vals = [50, 100, 200, 400, 800]
m = 50
p = 0.3
seeds   = list(range(500))
c=2

fieldnames = ['n', 'm', 'p', 'seed', 'algoritmo',
              'n_iter',                      
              'dim_cover',      
              'valid']

# output CSV
output_path = os.path.join(os.path.dirname(__file__), 
              '..', 'risultati', 'exp_rand_lv_vs_mc.csv')
os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for n in n_vals:
        for seed in seeds:
            X, F = generate_instance_bernoulli(n, m, p, seed)

            # esegui ogni algoritmo e scrivi una riga
            for alg, func in [ ('Las Vegas', randomized_rounding_las_vegas),
                            ('Monte Carlo', randomized_rounding)]:
                try:
                    if alg=='Las Vegas':
                        cover, n_iter=randomized_rounding_las_vegas(X, F, seed=seed)
                        
                    else:
                        cover=randomized_rounding(X,F, c=c, seed=seed)
                        n_iter=math.ceil(c * math.log(n))
                    
                    dim_cover=len(cover) if cover is not None else None
                    valid=is_valid_cover(X,F, cover) if cover is not None else False
                
                except Exception as e:
                    print(f"Errore LV (n={n}, seed={seed}): {e}")
                    n_iter, dim_cover, valid = None, None, False
                    
                writer.writerow({
                            'n': n,
                            'm': m,
                            'p': p,
                            'seed': seed,
                            'algoritmo': alg,
                            'n_iter':n_iter,
                            'dim_cover': dim_cover,
                            'valid': valid
                        })

print(f"Esperimento completato. Risultati salvati in {output_path}")

