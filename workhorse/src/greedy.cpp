#include "greedy.h"
#include <vector>
#include <set>

std::vector<int> greedy_set_cover(
    const std::set<int>& universo,
    const std::vector<std::set<int>>& F)
{
    std::set<int> covered;
    std::vector<int> selected;
    int m = F.size();

    while (covered != universo) {
        int best_idx  = -1;
        int best_gain = 0;

        for (int j = 0; j < m; j++) {
            int gain = 0;
            for (int e : F[j]) {
                if (covered.find(e) == covered.end())
                    gain++;
            }
            if (gain > best_gain) {
                best_gain = gain;
                best_idx  = j;
            }
        }

        if (best_idx == -1) break; // universo non copribile

        selected.push_back(best_idx);
        for (int e : F[best_idx])
            covered.insert(e);
    }

    return selected;
}