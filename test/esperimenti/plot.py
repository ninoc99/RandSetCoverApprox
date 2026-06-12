import pandas as pd
import matplotlib.pyplot as plt
import os

BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
DATA_DIR = os.path.join(BASE_DIR, "risultati")
OUTPUT_DIR = os.path.join(BASE_DIR, "risultati/plot")


def _save(fig, filename):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = os.path.join(OUTPUT_DIR, filename)
    fig.savefig(path, bbox_inches="tight", dpi=150)
    plt.close(fig)
    print(f"  [OK] {path}")

#ESP. 1: Confronto qualità soluzione Algoritmo Esatto vs Greedy vs Randomized
def plotEsp1():

    df = pd.read_csv(os.path.join(DATA_DIR, 'exp1_quality.csv'))

    fig, ax = plt.subplots(figsize=(12, 5))

    # Plot 1: rho medio per p, per algoritmo
    rho_p = df.groupby(['algoritmo', 'p'])['rho'].mean().unstack('algoritmo')
    rho_p[['Greedy', 'Randomized']].plot(
        kind='bar', ax=ax, 
        color=['steelblue', 'tomato'],
        yerr=df.groupby(['algoritmo', 'p'])['rho'].std().unstack('algoritmo')[['Greedy', 'Randomized']],
        capsize=4
    )
    ax.set_title('Rapporto di approssimazione medio per p')
    ax.set_xlabel('p')
    ax.set_ylabel('ρ medio')
    ax.axhline(y=1.0, color='black', linestyle='--', linewidth=0.8, label='OPT')
    ax.legend()
    ax.set_xticklabels([0.2, 0.3, 0.5], rotation=0)

    _save(fig, "esp_01_rapp_approx_medio.png")

    # Plot 2: rho medio per n, per algoritmo
    fig, ax=plt.subplots(figsize=(12,5))

    rho_n = df.groupby(['algoritmo', 'n'])['rho'].mean().unstack('algoritmo')
    rho_n[['Greedy', 'Randomized']].plot(
        kind='line', ax=ax, marker='o',
        color=['steelblue', 'tomato']
    )
    ax.set_title('Rapporto di approssimazione medio per n')
    ax.set_xlabel('n')
    ax.set_ylabel('ρ medio')
    ax.axhline(y=1.0, color='black', linestyle='--', linewidth=0.8, label='OPT')
    ax.legend()

    _save(fig, "esp_01_rho_medio_x_n.png")

    return None

#ESP. 2: Valutazione andamento temporale Greedy vs Randomized
def plotEsp2(file='exp2_runtime.csv'):

    df = pd.read_csv(os.path.join(DATA_DIR, 'exp2_runtime.csv'))

    fig, ax= plt.subplots(figsize=(12, 5))

    # Plot 1: tempo medio per n (scala lineare)
    tempo_n = df.groupby(['algoritmo', 'n'])['tempo_sec'].mean().unstack('algoritmo')
    tempo_n.plot(ax=ax, marker='o', color=['steelblue', 'tomato'])
    ax.set_title('Tempo medio per n (scala lineare)')
    ax.set_xlabel('n')
    ax.set_ylabel('Tempo (sec)')
    ax.legend(['Greedy', 'Randomized'])

    _save(fig, "esp_02_t_medio_lineare.png")

    # Plot 2: tempo medio per n (scala log-log)

    fig,ax=plt.subplots(figsize=(12,5))

    tempo_n.plot(ax=ax, marker='o', color=['steelblue', 'tomato'],
                loglog=True)
    ax.set_title('Tempo medio per n (scala log-log)')
    ax.set_xlabel('n')
    ax.set_ylabel('Tempo (sec)')
    ax.legend(['Greedy', 'Randomized'])

    _save(fig, "esp_02_t_medio_log.png")

    # Plot 3: tempo medio per m (n fisso)

    fig, ax = plt.subplots(figsize=(12, 5))

    #Plot 3: tempo in funzione di m (numero insiemi - n fisso)
    tempo_m = df.groupby(['algoritmo', 'm'])['tempo_sec'].mean().unstack('algoritmo')
    tempo_m.plot(ax=ax, marker='o', color=['steelblue', 'tomato'])
    ax.set_title('Tempo medio per m (a n variabile)')
    ax.set_xlabel('m')
    ax.set_ylabel('Tempo (sec)')
    ax.legend(['Greedy', 'Randomized'])

    _save(fig, "esp_02_t_medio_x_m.png")

    return None

#ESP. 3: Analisi Worst case Greedy 
def plotWorstCase():

    df = pd.read_csv(os.path.join(DATA_DIR, 'exp_wc.csv'))

    fig, ax = plt.subplots(figsize=(12, 5))

    for alg, color, marker in [
        ('Brute Force', 'green', 's'),
        ('ILP',         'purple', 'D'),
        ('Greedy',      'steelblue', 'o'),
        ('Randomized',  'tomato', '^')
    ]:
        subset = df[df['algoritmo'] == alg]
        ax.plot(subset['k'], subset['rho'],
                label=alg, color=color, marker=marker)

    ax.axhline(y=1.0, color='black', linestyle='--',
               linewidth=0.8, label='OPT')
    ax.set_title('Rapporto di approssimazione sul worst-case al variare di k')
    ax.set_xlabel('k')
    ax.set_ylabel('ρ = dim_cover / OPT')
    ax.set_xticks([3,4,5,6,7,8])
    ax.legend()

    _save(fig, "esp_03_worstcase.png")

    return None

#ESP. 4: Analisi variabilità seed nel Randomized Rounding
def plotVarSeedRand():

    df = pd.read_csv(os.path.join(DATA_DIR, 'exp4_var_rand.csv'))

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Plot 1: istogramma distribuzione dim_cover
    rand = df[df['algoritmo'] == 'Randomized']['dim_cover']
    greedy_val = df[df['algoritmo'] == 'Greedy']['dim_cover'].iloc[0]

    axes[0].hist(rand, bins=range(rand.min(), rand.max()+2),
                 color='tomato', alpha=0.7, edgecolor='black',
                 label='Randomized')
    axes[0].axvline(x=greedy_val, color='steelblue', linewidth=2,
                    linestyle='--', label=f'Greedy (fisso = {greedy_val})')
    axes[0].axvline(x=rand.mean(), color='darkred', linewidth=1.5,
                    linestyle=':', label=f'E[|C|] = {rand.mean():.1f}')
    axes[0].set_title('Distribuzione di |C| su 200 esecuzioni\n(stessa istanza, seed diversi)')
    axes[0].set_xlabel('|C| (dimensione cover)')
    axes[0].set_ylabel('frequenza')
    axes[0].legend()

    # Plot 2: dim_cover per seed (serie temporale)
    axes[1].plot(rand.values, color='tomato', alpha=0.7,
                 linewidth=0.8, label='Randomized')
    axes[1].axhline(y=greedy_val, color='steelblue', linewidth=2,
                    linestyle='--', label=f'Greedy (fisso = {greedy_val})')
    axes[1].axhline(y=rand.mean(), color='darkred', linewidth=1.5,
                    linestyle=':', label=f'E[|C|] = {rand.mean():.1f}')
    axes[1].set_title('|C| per seed (stessa istanza)')
    axes[1].set_xlabel('seed')
    axes[1].set_ylabel('|C|')
    axes[1].legend()

    _save(fig, "esp_04_varSeedRand.png")

    return None

#ESP. 5: Analisi della probabilità di errore (c) del Randomized Rounding
def plotRoundRand():

    df = pd.read_csv(os.path.join(DATA_DIR, 'exp5_n_round.csv'))

    summary = df.groupby('c').agg(
        t=('t', 'first'),
        tasso=('valid', 'mean'),
        media=('dim_cover', 'mean'),
        std=('dim_cover', 'std')
    ).reset_index()

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Plot 1: tasso di successo per c
    axes[0].bar(summary['c'], summary['tasso'] * 100,
                color='steelblue', edgecolor='black', alpha=0.8)
    axes[0].axhline(y=100, color='black', linestyle='--', linewidth=0.8)
    axes[0].set_title('Tasso di successo (valid=True)\nal variare di c')
    axes[0].set_xlabel('c')
    axes[0].set_ylabel('% esecuzioni con copertura valida')
    axes[0].set_xticks([1, 2, 3, 4])
    axes[0].set_ylim(80, 101)
    for i, row in summary.iterrows():
        axes[0].text(row['c'], row['tasso']*100 + 0.3,
                     f"t={int(row['t'])}", ha='center', fontsize=9)

    # Plot 2: media e std di |C| per c
    axes[1].errorbar(summary['c'], summary['media'],
                     yerr=summary['std'], fmt='o-',
                     color='tomato', capsize=5, linewidth=2,
                     label='media ± std')
    axes[1].set_title('Dimensione media della cover\nal variare di c')
    axes[1].set_xlabel('c')
    axes[1].set_ylabel('|C| medio')
    axes[1].set_xticks([1, 2, 3, 4])
    axes[1].legend()

    _save(fig, "esp_05_roundRand.png")

    return None

#ESP. 6: Analisi del tasso di fallimento empirico vs bound teorico del Randomized Rounding
def plotFailRate():

    df = pd.read_csv(os.path.join(DATA_DIR, 'exp6_fail_rate.csv'))

    # Aggregazione per (n, c)
    summary = df.groupby(['n', 'c']).agg(
        valid_mean=('valid', 'mean')
    ).reset_index()
    
    summary['fail_emp'] = 1 - summary['valid_mean']
    summary['bound_teo'] = summary['n'].astype(float) ** (1 - summary['c'])
    summary['ratio'] = summary['fail_emp'] / summary['bound_teo']

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Plot 1: tasso di fallimento empirico vs bound teorico per c
    colors = ['steelblue', 'tomato', 'green', 'purple']
    for idx, c in enumerate(sorted(summary['c'].unique())):
        subset = summary[summary['c'] == c].sort_values('n')
        axes[0].plot(subset['n'], subset['fail_emp'], marker='o',
                     label=f'empirico (c={c})', color=colors[idx],
                     linewidth=2, alpha=0.8)
        axes[0].plot(subset['n'], subset['bound_teo'], marker='s',
                     linestyle='--', color=colors[idx],
                     label=f'teorico (c={c})', alpha=0.6, linewidth=1.5)

    axes[0].set_title('Tasso di fallimento empirico vs bound teorico')
    axes[0].set_xlabel('n')
    axes[0].set_ylabel('Tasso di fallimento')
    axes[0].set_yscale('log')
    axes[0].legend(fontsize=9)
    axes[0].grid(True, alpha=0.3)

    # Plot 2: ratio empirico/teorico per c
    for idx, c in enumerate(sorted(summary['c'].unique())):
        subset = summary[summary['c'] == c].sort_values('n')
        axes[1].plot(subset['n'], subset['ratio'], marker='o',
                     label=f'c={c}', color=colors[idx], linewidth=2)

    axes[1].axhline(y=1.0, color='black', linestyle='--',
                    linewidth=0.8, label='Bound stretto')
    axes[1].set_title('Ratio: tasso empirico / bound teorico')
    axes[1].set_xlabel('n')
    axes[1].set_ylabel('Ratio')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    _save(fig, "esp_06_failRate.png")

    return None

#ESP. 6: Trade off - Prob.errore vs |C| medio
def plottradeOffRoundRand():

    df = pd.read_csv(os.path.join(DATA_DIR,'exp6_fail_rate.csv'))

    fig, axes = plt.subplots(2, 3, figsize=(15, 8))

    for idx, c in enumerate([1, 2, 3]):
        subset = df[df['c'] == c]
        summary = subset.groupby('n').agg(
            fail=('valid', lambda x: 1 - x.mean()),
            media_cover=('dim_cover', 'mean')
        ).reset_index()

        fail_plot = summary['fail'].replace(0, 1e-5)

        # riga 0: tasso fallimento
        axes[0, idx].semilogy(summary['n'], fail_plot,
                              color='tomato', marker='o')
        axes[0, idx].set_title(f'c={c}  (t=⌈{c}·ln n⌉)')
        axes[0, idx].set_ylabel('tasso fallimento (log)')
        axes[0, idx].set_xlabel('n')
        axes[0, idx].grid(True, alpha=0.3)

        # riga 1: dimensione media
        axes[1, idx].plot(summary['n'], summary['media_cover'],
                          color='steelblue', marker='s', linestyle='--')
        axes[1, idx].set_ylabel('|C| medio')
        axes[1, idx].set_xlabel('n')
        axes[1, idx].grid(True, alpha=0.3)

    _save(fig, 'esp_06_tradeoff_totale.png')

    return None

#ESP. 7: Analisi distribuzione della soluzione |C| per n variabile nel Randomized Rounding
def plotDistrbCover():

    df = pd.read_csv(os.path.join(DATA_DIR,'exp7_distrib_cover.csv'))

    n_vals = sorted(df['n'].unique())
    colors = plt.cm.viridis([i / len(n_vals) for i in range(len(n_vals))])

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Plot 1: istogrammi sovrapposti
    for i, n in enumerate(n_vals):
        subset = df[df['n'] == n]['dim_cover']
        axes[0].hist(subset, bins=range(int(subset.min()), int(subset.max())+2),
                     alpha=0.5, color=colors[i], label=f'n={n}',
                     edgecolor='black', linewidth=0.3)

    axes[0].set_title('Distribuzione di |C| al variare di n\n(Randomized Rounding, c=2, 500 seed)')
    axes[0].set_xlabel('|C| (dimensione cover)')
    axes[0].set_ylabel('frequenza')
    axes[0].legend()

    # Plot 2: media e std per n
    summary = df.groupby('n')['dim_cover'].agg(['mean', 'std']).reset_index()
    axes[1].errorbar(summary['n'], summary['mean'],
                     yerr=summary['std'], fmt='o-',
                     color='steelblue', capsize=5, linewidth=2,
                     label='media ± std')
    axes[1].set_title('Media e deviazione standard di |C| per n')
    axes[1].set_xlabel('n')
    axes[1].set_ylabel('|C|')
    axes[1].legend()

    _save(fig, 'esp_07_distrib_cover.png')

    return None

#Esp. 8: Pattern Hash-map: confronto con greedy naive
def plotHashMapGreedy():
    
    df = pd.read_csv(os.path.join(DATA_DIR,'exp8_greedy_hashmap.csv'))

    fig, axes = plt.subplots(1, 3, figsize=(16, 5))

    # Plot 1: tempo per n (scala log-log)
    tempo_n = df.groupby(['algoritmo', 'n'])['tempo_sec'].mean().unstack('algoritmo')
    tempo_n.plot(ax=axes[0], marker='o', loglog=True,
                 color=['steelblue', 'tomato'])
    axes[0].set_title('Tempo medio per n (log-log)')
    axes[0].set_xlabel('n')
    axes[0].set_ylabel('Tempo (sec)')
    axes[0].legend(['Greedy', 'Greedy Hash-Map'])

    # Plot 2: tempo per p
    tempo_p = df.groupby(['algoritmo', 'p'])['tempo_sec'].mean().unstack('algoritmo')
    tempo_p.plot(ax=axes[1], kind='bar', color=['steelblue', 'tomato'],
                 edgecolor='black', alpha=0.8)
    axes[1].set_title('Tempo medio per p')
    axes[1].set_xlabel('p')
    axes[1].set_ylabel('Tempo (sec)')
    axes[1].set_xticklabels([0.1, 0.3, 0.5], rotation=0)
    axes[1].legend(['Greedy', 'Greedy Hash-Map'])

    # Plot 3: speedup per n
    speedup = tempo_n['Greedy'] / tempo_n['Greedy Hash-Map']
    axes[2].plot(speedup.index, speedup.values,
                 color='green', marker='o', linewidth=2)
    axes[2].axhline(y=1.0, color='black', linestyle='--',
                    linewidth=0.8, label='no speedup')
    axes[2].set_title('Speedup (Greedy / Hash-Map) per n')
    axes[2].set_xlabel('n')
    axes[2].set_ylabel('Speedup')
    axes[2].legend()

    _save(fig, 'esp_08_hashmap_greedy.png')

    return None

#Esp. 9: Confronto Randomized Rounding: Las Vegas vs Monte Carlo
def plotLVvsMC():

    df = pd.read_csv(os.path.join(DATA_DIR, 'exp_rand_lv_vs_mc.csv'))

    lv = df[df['algoritmo'] == 'Las Vegas']
    mc = df[df['algoritmo'] == 'Monte Carlo']

    fig, axes = plt.subplots(1, 3, figsize=(16, 5))

    # Plot 1: iterazioni medie LV vs round fissi MC per n (scala log)
    lv_mean = lv.groupby('n')['n_iter'].mean()
    mc_iter = mc.groupby('n')['n_iter'].mean()

    axes[0].semilogy(lv_mean.index, lv_mean.values,
                     marker='o', color='tomato', label='Las Vegas (iter medie)')
    axes[0].semilogy(mc_iter.index, mc_iter.values,
                     marker='s', color='steelblue', linestyle='--', label='Monte Carlo (round fissi)')
    axes[0].set_title('Iterazioni medie: Las Vegas vs Monte Carlo\n(scala log)')
    axes[0].set_xlabel('n')
    axes[0].set_ylabel('n_iter (log)')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    # Plot 2: distribuzione iterazioni Las Vegas (boxplot per n)
    lv_data = [lv[lv['n'] == n]['n_iter'].values for n in sorted(lv['n'].unique())]
    axes[1].boxplot(lv_data, tick_labels=sorted(lv['n'].unique()), showfliers=False)
    axes[1].set_title('Distribuzione iterazioni Las Vegas per n\n(outlier esclusi)')
    axes[1].set_xlabel('n')
    axes[1].set_ylabel('n_iter')
    axes[1].grid(True, alpha=0.3)

    # Plot 3: dimensione media cover per algoritmo e n
    lv_dim = lv.groupby('n')['dim_cover'].mean()
    mc_dim = mc.groupby('n')['dim_cover'].mean()

    axes[2].plot(lv_dim.index, lv_dim.values,
                 marker='o', color='tomato', label='Las Vegas')
    axes[2].plot(mc_dim.index, mc_dim.values,
                 marker='s', color='steelblue', linestyle='--', label='Monte Carlo (c=2)')
    axes[2].set_title('Dimensione media cover per n')
    axes[2].set_xlabel('n')
    axes[2].set_ylabel('|C| medio')
    axes[2].legend()
    axes[2].grid(True, alpha=0.3)

    _save(fig, 'esp_09_LasVegasvsMonteCarlo.png')

    return None



if __name__ == '__main__':

   
    print("PLOT ESP. 1: Valutazione qualità soluzione tra algoritmi esatti e di approssimazione")
    plotEsp1()
    print("PLOT ESP. 2: Valutazione andamento temporale Greedy vs Randomized")
    plotEsp2()
    print("PLOT ESP. 3: Valutazione qualità soluzione nel Worst Case")
    plotWorstCase()
    print("PLOT ESP. 4: Valutazione della variabilità del Randomized Rounding al variare del seed")
    plotVarSeedRand()
    print("PLOT ESP. 5: Studio di come il n° di round (t=c*ln(n)) del Randomized Alg. influenza la qualità della soluzione.")
    plotRoundRand()
    print("PLOT ESP. 6: Analisi tasso di fallimento vs bound teorico")
    plotFailRate()
    print("PLOT ESP. 6: Trad off - Ammissibilità vs costo del Randomized Rounding ")
    plottradeOffRoundRand()
    print("PLOT ESP. 7: Distribuzione di |C| al variare di n")
    plotDistrbCover()
    print("PLOT ESP. 8: Confronto tra Greedy Naive e Greedy con HashMap")
    plotHashMapGreedy()
    print("PLOT ESP. 9: Confronto Randomized Rounding: Las Vegas vs Monte Carlo")
    plotLVvsMC()
