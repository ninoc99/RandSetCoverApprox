import pandas as pd
import matplotlib.pyplot as plt
import os

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "risultati")
PLOT_DIR = os.path.join(BASE_DIR, "risultati", "plot")
os.makedirs(PLOT_DIR, exist_ok=True)

def _save(fig, filename):
    os.makedirs(PLOT_DIR, exist_ok=True)
    path = os.path.join(PLOT_DIR, filename)
    fig.savefig(path, bbox_inches="tight", dpi=150)
    plt.close(fig)
    print(f"  [OK] {path}")


def plotWorkhorse():

    df = pd.read_csv(os.path.join(DATA_DIR,'workhorse_results.csv'))

    fig, axes = plt.subplots(1, 3, figsize=(16, 5))

    # Plot 1: tempo per n (log-log) per tutti e tre gli algoritmi
    tempo_n = df.groupby(['algoritmo', 'n'])['tempo_sec'].mean().unstack('algoritmo')
    colors = {'Greedy': 'steelblue', 'GreedyHashMap': 'tomato', 'Randomized': 'green'}
    for alg in ['Greedy', 'GreedyHashMap', 'Randomized']:
        axes[0].loglog(tempo_n.index, tempo_n[alg],
                       marker='o', label=alg, color=colors[alg])
    axes[0].set_title('Tempo medio per n (log-log)\nWorkhorse C++')
    axes[0].set_xlabel('n')
    axes[0].set_ylabel('Tempo (sec)')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    # Plot 2: speedup GreedyHashMap vs Greedy per n
    speedup_n = tempo_n['Greedy'] / tempo_n['GreedyHashMap']
    axes[1].plot(speedup_n.index, speedup_n.values,
                 marker='o', color='purple', linewidth=2)
    axes[1].axhline(y=1.0, color='black', linestyle='--', linewidth=0.8)
    axes[1].set_title('Speedup GreedyHashMap vs Greedy\nper n')
    axes[1].set_xlabel('n')
    axes[1].set_ylabel('Speedup')
    axes[1].grid(True, alpha=0.3)

    # Plot 3: speedup per p
    tempo_p = df.groupby(['algoritmo', 'p'])['tempo_sec'].mean().unstack('algoritmo')
    speedup_p = tempo_p['Greedy'] / tempo_p['GreedyHashMap']
    axes[2].bar([0.1, 0.3, 0.5], speedup_p.values,
                width=0.08, color='purple', alpha=0.8, edgecolor='black')
    axes[2].axhline(y=1.0, color='black', linestyle='--', linewidth=0.8)
    axes[2].set_title('Speedup GreedyHashMap vs Greedy\nper p')
    axes[2].set_xlabel('p (densità)')
    axes[2].set_ylabel('Speedup')
    axes[2].set_xticks([0.1, 0.3, 0.5])
    axes[2].grid(True, alpha=0.3)

    _save(fig, 'workhorse_analisi.png')


    return None

def plotWHQual():

    df = pd.read_csv(os.path.join(DATA_DIR, 'workhorse_results.csv'))

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Plot 1: dimensione media per n
    quality_n = df.groupby(['algoritmo', 'n'])['dim_cover'].mean().unstack('algoritmo')
    colors = {'Greedy': 'steelblue', 'GreedyHashMap': 'tomato', 'Randomized': 'green'}
    for alg in ['Greedy', 'GreedyHashMap', 'Randomized']:
        axes[0].plot(quality_n.index, quality_n[alg],
                     marker='o', label=alg, color=colors[alg])
    axes[0].set_title('Dimensione media cover per n\n(Workhorse C++)')
    axes[0].set_xlabel('n')
    axes[0].set_ylabel('|C| medio')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    # Plot 2: rapporto Randomized / Greedy per n
    ratio = quality_n['Randomized'] / quality_n['Greedy']
    axes[1].plot(ratio.index, ratio.values,
                 marker='o', color='purple', linewidth=2)
    axes[1].axhline(y=1.0, color='black', linestyle='--',
                    linewidth=0.8, label='parità con Greedy')
    axes[1].set_title('Rapporto |C| medio: Randomized / Greedy\nper n (Workhorse C++)')
    axes[1].set_xlabel('n')
    axes[1].set_ylabel('Rapporto')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    
    _save(fig, 'WH_qual.png')

    return None


def plotDoublingExperiment():

    df = pd.read_csv(os.path.join(DATA_DIR, 'workhorse_results.csv'))

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    colors = {'Greedy': 'steelblue', 'GreedyHashMap': 'tomato', 'Randomized': 'green'}
    algs = ['Greedy', 'GreedyHashMap', 'Randomized']

    # Plot 1: rapporto C(2n)/C(n) per n (m=50 fisso)
    sub_n = df[df['m'] == 50].groupby(['algoritmo', 'n'])['tempo_sec'].mean().unstack('algoritmo')
    n_vals = sorted(sub_n.index)

    for alg in algs:
        ratios = [sub_n[alg][n_vals[i]] / sub_n[alg][n_vals[i-1]]
                  for i in range(1, len(n_vals))]
        axes[0].plot(n_vals[1:], ratios,
                     marker='o', label=alg, color=colors[alg], linewidth=2)

    axes[0].axhline(y=2.0, color='black', linestyle='--',
                    linewidth=0.8, label='rapporto=2 (O(n))')
    axes[0].set_xscale('log', base=2)
    axes[0].set_xticks(n_vals[1:])
    axes[0].set_xticklabels(n_vals[1:], rotation=45)
    axes[0].set_title('Doubling experiment: raddoppio di n\n(m=50 fisso)')
    axes[0].set_xlabel('n')
    axes[0].set_ylabel('C(2n) / C(n)')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    # Plot 2: rapporto C(2m)/C(m) per n fisso (m: 50->100)
    n_fissi = sorted(df[df['m'].isin([50, 100])]['n'].unique())
    # escludi il primo valore perché non ha un precedente per il rapporto
    n_fissi = [n for n in n_fissi if n >= 200]    
    width = 0.25
    x = range(len(n_fissi))

    for idx, alg in enumerate(algs):
        ratios_m = []
        for n in n_fissi:
            sub = df[(df['n'] == n) & (df['m'].isin([50, 100]))]\
                .groupby(['algoritmo', 'm'])['tempo_sec'].mean().unstack('algoritmo')
            ratios_m.append(sub[alg][100] / sub[alg][50])
        axes[1].bar([xi + idx*width for xi in x], ratios_m,
                    width=width, label=alg, color=colors[alg],
                    alpha=0.8, edgecolor='black')

    axes[1].axhline(y=2.0, color='black', linestyle='--',
                    linewidth=0.8, label='rapporto=2 (O(m))')
    axes[1].set_title('Doubling experiment: raddoppio di m\n(m: 50->100, n variabile)')
    axes[1].set_xlabel('n')
    axes[1].set_ylabel('C(2m) / C(m)')
    axes[1].set_xticks([xi + width for xi in x])
    axes[1].set_xticklabels(n_fissi, rotation=45)
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    
    _save(fig, 'doublingExp.png')

    return None


def plotGreedyVsRandomized():

    df = pd.read_csv(os.path.join(DATA_DIR, 'workhorse_results.csv'))
    colors = {'Greedy': 'steelblue', 'Randomized': 'green'}

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Plot 1: tempo per n (log-log) solo Greedy vs Randomized
    sub = df[(df['m'] == 50) & (df['p'] == 0.3)]
    tempo_n = sub.groupby(['algoritmo', 'n'])['tempo_sec'].mean().unstack('algoritmo')

    for alg in ['Greedy', 'Randomized']:
        axes[0].loglog(tempo_n.index, tempo_n[alg],
                       marker='o', label=alg, color=colors[alg])
    
    axes[0].set_title('Runtime: Greedy vs Randomized\n(log-log, m=50, p=0.3)')
    axes[0].set_xlabel('n')
    axes[0].set_ylabel('Tempo (sec)')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    # Plot 2: rapporto Randomized / Greedy per n
    ratio = tempo_n['Randomized'] / tempo_n['Greedy']
    axes[1].plot(tempo_n.index, ratio.values,
                 marker='o', color='purple', linewidth=2)
    axes[1].axhline(y=1.0, color='black', linestyle='--',
                    linewidth=0.8, label='parita\'')
    axes[1].set_title('Rapporto runtime: Randomized / Greedy per n')
    axes[1].set_xlabel('n')
    axes[1].set_ylabel('Rapporto')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    plt.suptitle('Greedy vs Randomized Rounding', fontsize=13)
    plt.tight_layout()
    _save(fig, 'greedy_vs_randomized.png')

    return None

if __name__ == '__main__':
    plotWorkhorse()
    plotWHQual()
    plotDoublingExperiment()
    plotGreedyVsRandomized()