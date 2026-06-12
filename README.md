# Approximate Set Cover via Randomization

## Descrizione

Implementazione e valutazione sperimentale di algoritmi di approssimazione 
per il problema Set Cover con focus sulle tecniche di randomizzazione.

### Algoritmi studiati:

- Brute force
- ILP (Integer Linear Programming)
- Greedy deterministico
- Greedy con pattern Hash Map (Reduce-to-Hash-Tables)
- Randomized Rounding — Monte Carlo
- Randomized Rounding — Las Vegas

La metodologia segue l'approccio dell'Algorithm Engineering:
fase **pilot** (Python) e fase **workhorse** (C++).

---

## Struttura del progetto

```text
SetCover_RandomApprox/
├── test/                        # Fase pilot (Python)
│   ├── algoritmi/               # Implementazioni algoritmi
│   │   ├── brute_force.py
│   │   ├── greedy.py
│   │   ├── greedy_hash_pattern.py
│   │   ├── ilp.py
│   │   ├── lp_solver.py
│   │   ├── randomized.py
│   │   └── randomized_las_vegas.py
│   ├── esperimenti/             # Script esperimenti
│   │   ├── exp_qs.py
│   │   ├── exp_rt.py
│   │   ├── exp_wc.py
│   │   ├── exp3_var.py
│   │   ├── exp5_param_c.py
│   │   ├── exp6_fail_rate.py
│   │   ├── exp7_distrib.py
│   │   ├── exp_hashmap.py
│   │   ├── exp9_bottleneckRoundRand.py
│   │   ├── exp_lv_vs_mc.py
│   │   ├── analisi.py
│   │   └── plot.py
│   ├── risultati/               # CSV e plot
│   │   └── plot/
│   ├── utils.py
│   └── regression_test.py
├── workhorse/                   # Fase workhorse (C++)
│   ├── src/
│   │   ├── generator.h/cpp
│   │   ├── greedy.h/cpp
│   │   ├── greedy_hashmap.h/cpp
│   │   ├── randomized.h/cpp
│   │   ├── exp_runtime.h/cpp
│   │   ├── exp_bottleneck.h/cpp
│   │   └── main.cpp
│   ├── risultati/
│   │   └── plot/
│   ├── analisi.py
│   ├── plot.py
│   └── Makefile
└── report/                      # Documentazione e relazioni finali
    ├── report.pdf
    ├── report.tex
    ├── plot/
    └── img/

```

---

## Requisiti

- Python 3.10+
- Visual Studio Code con estensione Python
- Ambiente virtuale (`.venv`)

###Librerie e dipendenze

Python:
- pulp
- pandas 
- matplotlib
- gurobipy

C++:
- clang++
- GLPK 5.0

## Istruzioni d'uso

### Regression test (verifica correttezza)

```bash
cd test
source .venv/bin/activate
python3 regression_test.py
```

### Esperimenti pilot

```bash
cd test
source .venv/bin/activate

# stampa risultati e plot degli esperimenti
python3 esperimenti/analisi.py
python3 esperimenti/plot.py
```

### Workhorse C++

```bash
cd workhorse

# esperimento runtime (W1, W2, W3)
./setcover runtime

# esperimento bottleneck (W4)
./setcover bottleneck

# tutti gli esperimenti
./setcover all
```

I risultati sono salvati in `workhorse/risultati/`.

### Analisi e plot workhorse

```bash
cd workhorse
source ../.venv/bin/activate   # oppure usa il venv globale
python3 analisi.py
python3 plot.py
```

---

## Hardware e software utilizzato

| Componente | Dettaglio |
|---|---|
| Hardware | MacBook Air, Apple Silicon M-series (arm64) |
| OS | macOS |
| IDE | Visual Studio Code |
| Python | 3.10+, ambiente virtuale `.venv` |
| Solver LP pilot | PuLP 3.3.2 con backend CBC |
| Solver ILP pilot | Gurobi (licenza accademica) |
| C++ | C++17, clang++ con flag `-O2` |
| Solver LP workhorse | GLPK 5.0 via Homebrew |
| Misurazione tempo | `std::clock()` (CPU time) |

---

## Report

Il report completo è disponibile in `report/report.pdf`.
Il sorgente LaTeX è in `report/report.tex`, compilabile con:

```bash
cd report
pdflatex report.tex
pdflatex report.tex
```

---

## Autore

Nino Giuseppe Critelli  
LM Ing. Informatica - DISIM
Università degli Studi dell'Aquila  
Anno Accademico 2025/2026