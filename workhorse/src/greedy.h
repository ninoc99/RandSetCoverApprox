#pragma once
#include <vector>
#include <set>

// Greedy Set Cover naive
// Complessità: O(n * m) per iterazione
// Ritorna: vettore di indici degli insiemi selezionati
std::vector<int> greedy_set_cover(
    const std::set<int>& universo,
    const std::vector<std::set<int>>& F
);