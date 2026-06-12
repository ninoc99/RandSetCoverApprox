#Confronto sull'andamento temporale tra Greedy naive e Greedy Hash Map

import csv
import time
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'algoritmi'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils import generate_instance_bernoulli, is_valid_cover
from greedy import greedy_set_cover
from greedy_hash_pattern import greedy_hashmap_setcover
from utils import *

# parametri esperimento
n_vals  = [100, 200, 400, 800, 1600, 3200, 6400, 12800]
m_vals  = [70, 140, 280]
p_vals  = [0.1, 0.3, 0.5]
seeds   = [42, 123, 7, 31, 999, 17, 53, 77, 101, 200]

fieldnames = ['n', 'm', 'p', 'seed',
              'algoritmo', 'dim_cover', 'tempo_sec', 'valid']

# output CSV
output_path = os.path.join(os.path.dirname(__file__), 
              '..', 'risultati', 'exp8_greedy_hashmap.csv')
os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for n in n_vals:
        for m in m_vals:
            for p in p_vals:
                for seed in seeds:
                    X, F = generate_instance_bernoulli(n, m, p, seed)
        
                    # esegui ogni algoritmo e scrivi una riga
                    for alg, func in [
                                    ('Greedy', greedy_set_cover),
                                    ('Greedy Hash-Map', greedy_hashmap_setcover)]:
                            try:
                                start=time.perf_counter() #Inizio misurazione timing
                                cover = func(X, F)
                                elapsed=time.perf_counter()-start #Tempo di esecuzione alg.

                                dim_cover=len(cover) if cover is not None else None
                                valid=is_valid_cover(X,F, cover) if cover is not None else False

                            except Exception as e:
                                print(f"Errore con {alg} (n={n}, m={m}, p={p}, seed={seed}): {e}")
                                elapsed, dim_cover, valid = None, None, False

                            writer.writerow({
                                'n': n,
                                'm': m,
                                'p': p,
                                'seed': seed,
                                'algoritmo': alg,
                                'dim_cover': dim_cover,
                                'tempo_sec': elapsed,
                                'valid': valid
                            })
print(f"Esperimento completato. Risultati salvati in {output_path}")

