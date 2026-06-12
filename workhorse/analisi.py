import pandas as pd
import matplotlib.pyplot as plt
import sys
import os


BASE_DIR = os.path.join(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "risultati")


def analisiWHRuntTIme():

    df = pd.read_csv(os.path.join(DATA_DIR, 'workhorse_results.csv'))

    print("\nANALISI SPEED UP Greedy vs Greedy Hash Map vs Randomized\n")

    # tempo medio per algoritmo e n
    tempo_n = df.groupby(['algoritmo', 'n'])['tempo_sec'].mean().unstack('algoritmo')
    print("Tempo medio per n (secondi):")
    print(tempo_n.to_string())

    # speedup greedy hashmap vs naive
    print("\nSpeedup GreedyHashMap vs Greedy per n:")
    ratio = tempo_n['Greedy'] / tempo_n['GreedyHashMap']
    print(ratio.to_string())

    # speedup per p
    tempo_p = df.groupby(['algoritmo', 'p'])['tempo_sec'].mean().unstack('algoritmo')
    print("\nTempo medio per p:")
    print(tempo_p.to_string())

    print("\nSpeedup GreedyHashMap vs Greedy per p:")
    ratio_p = tempo_p['Greedy'] / tempo_p['GreedyHashMap']
    print(ratio_p.to_string())

    # verifica validità
    print(f"\nCoperture valide: {df['valid'].sum()} su {len(df)}")

    return None


def analisiWHQuality():

    df = pd.read_csv(os.path.join(DATA_DIR, 'workhorse_results.csv'))

    print("\nANALISI QUALITÀ SOLUZIONE\n")

    # dimensione media per algoritmo e n
    quality_n = df.groupby(['algoritmo', 'n'])['dim_cover'].mean().unstack('algoritmo')
    print("Dimensione media cover per n:")
    print(quality_n.to_string())

    # rapporto Randomized / Greedy
    print("\nRapporto |C| medio: Randomized / Greedy per n:")
    ratio = quality_n['Randomized'] / quality_n['Greedy']
    print(ratio.to_string())

    # dimensione media per algoritmo e p
    quality_p = df.groupby(['algoritmo', 'p'])['dim_cover'].mean().unstack('algoritmo')
    print("\nDimensione media cover per p:")
    print(quality_p.to_string())

    return None

def analisiDoublingExperiment():

    df = pd.read_csv(os.path.join(DATA_DIR, 'workhorse_results.csv'))

    print("\nDOUBLING EXPERIMENT\n")

    # ── Analisi 1: raddoppio di n (m fisso a 50) ──────────────────
    print("Rapporto C(2n)/C(n) per algoritmo (m=50 fisso):")
    sub_n = df[df['m'] == 50].groupby(['algoritmo', 'n'])['tempo_sec'].mean().unstack('algoritmo')
    n_vals = sorted(sub_n.index)

    header = f"{'n':>6} {'Greedy':>10} {'GreedyHashMap':>14} {'Randomized':>12}"
    print(header)
    print("-" * 45)
    for i in range(1, len(n_vals)):
        n_curr = n_vals[i]
        n_prev = n_vals[i-1]
        row = {alg: sub_n[alg][n_curr] / sub_n[alg][n_prev]
               for alg in ['Greedy', 'GreedyHashMap', 'Randomized']}
        print(f"{n_curr:>6} {row['Greedy']:>10.3f} "
              f"{row['GreedyHashMap']:>14.3f} {row['Randomized']:>12.3f}")

    print("\nInterpretazione attesa:")
    print("  Greedy:        rapporto ~2   -> O(n) per iterazione")
    print("  GreedyHashMap: rapporto <2   -> O(n log n) o meno")
    print("  Randomized:    rapporto ~2   -> dominato da LP O(n)")

    # ── Analisi 2: raddoppio di m (n fisso a 800) ─────────────────
    print("\nRapporto C(2m)/C(m) per algoritmo (n=800 fisso, m in {50,100}):")
    sub_m = df[(df['n'] == 800) & (df['m'].isin([50, 100]))]\
        .groupby(['algoritmo', 'm'])['tempo_sec'].mean().unstack('algoritmo')

    print(f"{'m':>6} {'Greedy':>10} {'GreedyHashMap':>14} {'Randomized':>12}")
    print("-" * 45)
    print(f"{'50->100':>8} "
      f"{sub_m['Greedy'][100]/sub_m['Greedy'][50]:>10.3f} "
      f"{sub_m['GreedyHashMap'][100]/sub_m['GreedyHashMap'][50]:>14.3f} "
      f"{sub_m['Randomized'][100]/sub_m['Randomized'][50]:>12.3f}")

    print("\nInterpretazione attesa:")
    print("  Greedy:        rapporto ~2   -> O(m) per iterazione")
    print("  GreedyHashMap: rapporto ~2   -> O(m log m)")
    print("  Randomized:    rapporto ~2   -> LP cresce con m")

    return None


def analisiBottleneckRandRound():

    df = pd.read_csv(os.path.join(DATA_DIR, 'bottleneck_results.csv'))

    print("\nANALISI BOTTLENECK RANDOMIZED ROUNDING \n")

    # percentuale media per fase
    df['pct_lp']       = df['t_lp']       / df['t_totale'] * 100
    df['pct_round']    = df['t_round']     / df['t_totale'] * 100
    df['pct_verifica'] = df['t_verifica']  / df['t_totale'] * 100

    print("Percentuale media per fase:")
    print(f"  LP:       {df['pct_lp'].mean():.1f}%")
    print(f"  Rounding: {df['pct_round'].mean():.1f}%")
    print(f"  Verifica: {df['pct_verifica'].mean():.1f}%")

    # tempo medio per fase e n
    print("\nTempo medio per fase e n (m=50):")
    sub = df[df['m'] == 50].groupby('n')[['t_lp','t_round','t_verifica']].mean()
    print(sub.to_string())

    # tempo medio per fase e m
    print("\nTempo medio per fase e m (n=800):")
    sub_m = df[df['n'] == 800].groupby('m')[['t_lp','t_round','t_verifica']].mean()
    print(sub_m.to_string())
    
    return None

if __name__ == '__main__':

    analisiWHRuntTIme()

    analisiDoublingExperiment()
    
    analisiWHQuality()

    analisiBottleneckRandRound()