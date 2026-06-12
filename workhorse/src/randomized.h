#pragma once
#include <vector>
#include <set>

// Randomized Rounding per Set Cover
// Risolve il LP con GLPK e applica t = ceil(c * ln(n)) round
// Ritorna: vettore di indici degli insiemi selezionati
std::vector<int> randomized_rounding(
    const std::set<int>& universo,
    const std::vector<std::set<int>>& F,
    double c,
    int seed
);