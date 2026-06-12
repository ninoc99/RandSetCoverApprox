#include "greedy_hashmap.h"
#include <vector>
#include <set>
#include <unordered_map>
#include <queue>

std::vector<int> greedy_hashmap_setcover(
    const std::set<int>& universo,
    const std::vector<std::set<int>>& F)
{
    int m = F.size();

    // mappa inversa: elemento → lista di indici degli insiemi che lo contengono
    std::unordered_map<int, std::vector<int>> elemento_a_insiemi;
    for (int j = 0; j < m; j++)
        for (int e : F[j])
            elemento_a_insiemi[e].push_back(j);

    // guadagno corrente per ogni insieme
    std::vector<int> gain(m);
    for (int j = 0; j < m; j++)
        gain[j] = F[j].size();

    // max-heap: (gain, indice)
    std::priority_queue<std::pair<int,int>> heap;
    for (int j = 0; j < m; j++)
        heap.push({gain[j], j});

    std::set<int> covered;
    std::vector<int> selected;

    while (covered != universo && !heap.empty()) {

        auto [g, best_j] = heap.top();
        heap.pop();

        // lazy deletion: valore obsoleto
        if (g != gain[best_j]) {
            heap.push({gain[best_j], best_j});
            continue;
        }

        // guadagno zero — nessun insieme utile
        if (gain[best_j] == 0) break;

        selected.push_back(best_j);

        // elementi realmente nuovi coperti
        std::vector<int> newly_covered;
        for (int e : F[best_j])
            if (covered.find(e) == covered.end())
                newly_covered.push_back(e);

        for (int e : newly_covered) {
            covered.insert(e);
            for (int j : elemento_a_insiemi[e]) {
                if (j != best_j) {
                    gain[j]--;
                    // lazy: non aggiorniamo l'heap subito
                }
            }
        }
    }

    return selected;
}