import pandas as pd
import os


BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
DATA_DIR = os.path.join(BASE_DIR, "risultati")

#ESP. 1: Confronto qualità soluzione Algoritmo Esatto vs Greedy vs Randomized
def TestQual():

    df = pd.read_csv(os.path.join(DATA_DIR, 'exp1_quality.csv'))

    # media di rho per algoritmo e valore di p
    rho_summary = df.groupby(['algoritmo', 'p'])['rho'].agg(['mean', 'std']).reset_index()
    print(rho_summary)

    # rho medio per algoritmo e n
    rho_by_n = df.groupby(['algoritmo', 'n'])['rho'].mean().unstack('algoritmo')
    print("\nRho medio per n:")
    print(rho_by_n)

    # casi dove randomized > greedy
    peggio = df[df['algoritmo'] == 'Randomized']['rho'] > \
            df[df['algoritmo'] == 'Greedy']['rho'].values
    print(f"\nCasi dove Randomized > Greedy: {peggio.sum()} su {len(peggio)}")

    return None

#ESP. 2: Valutazione andamento temporale Greedy vs Randomized
def TestRunTime():

    df = pd.read_csv(os.path.join(DATA_DIR,'exp2_runtime.csv'))

    # tempo medio per algoritmo e n
    tempo_summary = df.groupby(['algoritmo', 'n'])['tempo_sec'].mean().unstack('algoritmo')
    print(tempo_summary)

    return None

#ESP. 3: Analisi Worst case Greedy 
def TestWorstCase():

    df = pd.read_csv(os.path.join(DATA_DIR, 'exp_wc.csv'))
        
    # tabella rho per algoritmo e k
    pivot = df.pivot(index='k', columns='algoritmo', values='rho')
    print("Rapporto di approssimazione per k:")
    print(pivot.to_string())
    
    # crescita del rho del greedy
    greedy = df[df['algoritmo'] == 'Greedy']
    print("\nCrescita rho Greedy:")
    for _, row in greedy.iterrows():
        print(f"  k={int(row['k'])}, n={int(row['n'])}, "
              f"rho={row['rho']:.2f}, "
              f"ln(n)={row['n'].__class__.__name__}")
    
    # confronto con bound teorico H(max|S|)
    print("\nConfronto con bound teorico H(2^k):")
    for _, row in greedy.iterrows():
        k = int(row['k'])
        max_s = 2**k
        H = sum(1/i for i in range(1, max_s+1))
        print(f"  k={k}, rho_emp={row['rho']:.2f}, "
              f"H(2^k)*OPT={H*2:.2f}")
        
    return None

#ESP. 4: Analisi variabilità seed nel Randomized Rounding
def varSeedRand():
    
    df = pd.read_csv(os.path.join(DATA_DIR, 'exp4_var_rand.csv'))
        
    for alg in ['Greedy', 'Randomized']:
        subset = df[df['algoritmo'] == alg]['dim_cover']
        print(f"{alg}:")
        print(f"  media:    {subset.mean():.2f}")
        print(f"  std:      {subset.std():.2f}")
        print(f"  min:      {subset.min()}")
        print(f"  max:      {subset.max()}")
        print(f"  valori unici: {sorted(subset.unique())}")

    return None

#ESP. 5: Analisi della probabilità di errore (c) del Randomized Rounding
def nRoundRand():

    df = pd.read_csv(os.path.join(DATA_DIR, 'exp5_n_round.csv'))
    
    print(f"{'c':>4} {'t':>4} {'tasso_ok':>10} {'media_|C|':>10} {'std_|C|':>8}")
    print("-" * 42)
    
    for c in sorted(df['c'].unique()):
        subset = df[df['c'] == c]
        t = subset['t'].iloc[0]
        tasso = subset['valid'].mean()
        media = subset['dim_cover'].mean()
        std = subset['dim_cover'].std()
        print(f"{c:>4} {t:>4} {tasso:>10.1%} {media:>10.2f} {std:>8.2f}")
    
    return None

#ESP. 6: Analisi del tasso di fallimento empirico vs bound teorico del Randomized Rounding
def randFailRate():

    df = pd.read_csv(os.path.join(DATA_DIR, 'exp6_fail_rate.csv'))
    
    print(f"{'n':>6} {'c':>3} {'t':>4} {'fail_emp':>10} {'bound_teo':>12} {'ratio':>8}")
    print("-" * 50)
    
    for n in sorted(df['n'].unique()):
        for c in sorted(df['c'].unique()):
            subset = df[(df['n'] == n) & (df['c'] == c)]
            t = subset['t'].iloc[0]
            fail_emp = 1 - subset['valid'].mean()
            bound_teo = float(n) ** (1 - c)
            ratio = fail_emp / bound_teo if bound_teo > 0 else float('inf')
            print(f"{n:>6} {c:>3} {t:>4} {fail_emp:>10.4f} {bound_teo:>12.4f} {ratio:>8.4f}")

    return None


#ESP. 7: Analisi distribuzione della soluzione |C| per n variabile nel Randomized Rounding
def distribCover():

    df = pd.read_csv(os.path.join(DATA_DIR, 'exp7_distrib_cover.csv'))
    
    print(f"{'n':>6} {'media':>8} {'std':>8} {'min':>6} {'max':>6} {'valid%':>8}")
    print("-" * 45)

    for n in sorted(df['n'].unique()):
        subset = df[df['n'] == n]
        media = subset['dim_cover'].mean()
        std   = subset['dim_cover'].std()
        mn    = subset['dim_cover'].min()
        mx    = subset['dim_cover'].max()
        valid = subset['valid'].mean() * 100
        print(f"{n:>6} {media:>8.2f} {std:>8.2f} {mn:>6} {mx:>6} {valid:>7.1f}%")

    return None

#Esp. 8: Pattern Hash-map: confronto con greedy naive
def hashMapGreedy():

    df = pd.read_csv(os.path.join(DATA_DIR, 'exp8_greedy_hashmap.csv'))
    
    # tempo medio per algoritmo e n
    tempo_n = df.groupby(['algoritmo', 'n'])['tempo_sec'].mean().unstack('algoritmo')
    print("Tempo medio per n:")
    print(tempo_n.to_string())

    # tempo medio per algoritmo e p
    tempo_p = df.groupby(['algoritmo', 'p'])['tempo_sec'].mean().unstack('algoritmo')
    print("\nTempo medio per p:")
    print(tempo_p.to_string())

    # rapporto speedup
    print("\nSpeedup (Greedy / Greedy Hash-Map) per n:")
    ratio = tempo_n['Greedy'] / tempo_n['Greedy Hash-Map']
    print(ratio.to_string())

    return None

#Esp. 9: Confronto Randomized Rounding: Las Vegas vs Monte Carlo
def analisiLVvsMC():

    df = pd.read_csv(os.path.join(DATA_DIR, 'exp_rand_lv_vs_mc.csv'))

    lv = df[df['algoritmo'] == 'Las Vegas']
    mc = df[df['algoritmo'] == 'Monte Carlo']

    # iterazioni Las Vegas per n
    print("Distribuzione iterazioni Las Vegas per n:")
    stats = lv.groupby('n')['n_iter'].agg(['mean', 'std', 'min', 'max'])
    print(stats.to_string())

    # round fissi Monte Carlo per n
    print("\nRound fissi Monte Carlo (t = ceil(2·ln(n))) per n:")
    print(mc.groupby('n')['n_iter'].mean().to_string())

    # tasso di successo Monte Carlo per n
    print("\nTasso di successo Monte Carlo per n:")
    print(mc.groupby('n')['valid'].mean().to_string())

    # dimensione media cover
    print("\nDimensione media cover per algoritmo e n:")
    print(df.groupby(['algoritmo', 'n'])['dim_cover'].mean().unstack('algoritmo').to_string())

    return None




if __name__ == '__main__':

    print("\nESPERIMENTO 1: Valutazione qualità soluzione tra algoritmi esatti e di approssimazione")
    TestQual()

    print("\nESPERIMENTO 2: Valutazione andamento temporale Greedy vs Randomized")
    TestRunTime()

    print("\nESPERIMENTO 3: Valutazione algoritmi su Worst Case")
    TestWorstCase()

    print("\nESPERIMENTO 4: Analisi variabilità soluzione del Randomized Rounding al variare del seed")
    varSeedRand()

    print("\nESPERIMENTO 5: Studio di come il n° di round (t=c*ln(n)) del Randomized Alg. influenza la qualità della soluzione. ")
    nRoundRand()

    print("\nESPERIMENTO 6: Analisi che valuta per il Round Randomized Alg. il tasso di fallimento empirico confrontato con il bound teorico n^(1-c)")
    randFailRate()

    print("\nESPERIMENTO 7: #Esperimento su come si distribuisce la soluzione di Randomized Rounding - n variabile")
    distribCover()

    print("\nESPERIMENTO 8: Confronto andamento temporale tra Greedy Naive e Greedy con Hash Map")
    hashMapGreedy()
    
    print ("\nESPERIMENTO 9: Confronto Randomized Rounding: Las Vegas vs Monte Carlo")
    analisiLVvsMC()



