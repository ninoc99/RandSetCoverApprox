#pragma once
#include <vector>
#include <set>

// Greedy Set Cover con Hash Map + Max-Heap (lazy deletion)
// Complessità: O(Σ|S_j| · log m)
// Ritorna: vettore di indici degli insiemi selezionati
std::vector<int> greedy_hashmap_setcover(
    const std::set<int>& universo,
    const std::vector<std::set<int>>& F
);