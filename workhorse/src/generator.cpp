#include "generator.h"
#include <random>
#include <set>
#include <vector>

std::pair<std::set<int>, std::vector<std::set<int>>>
generate_instance_bernoulli(int n, int m, double p, int seed) {

    // universo: {1, 2, ..., n}
    std::set<int> universo;
    for (int i = 1; i <= n; i++)
        universo.insert(i);

    std::mt19937 rng(seed);
    std::uniform_real_distribution<double> dist(0.0, 1.0);
    std::uniform_int_distribution<int> elem_dist(1, n);

    std::vector<std::set<int>> F(m);

    // costruisci insiemi con probabilità p
    for (int j = 0; j < m; j++) {
        for (int e = 1; e <= n; e++) {
            if (dist(rng) < p)
                F[j].insert(e);
        }
    }

    // garanzia di copertura: ogni elemento deve essere in almeno un insieme
    for (int e = 1; e <= n; e++) {
        bool covered = false;
        for (int j = 0; j < m; j++) {
            if (F[j].count(e)) { covered = true; break; }
        }
        if (!covered) {
            // aggiungi e a un insieme casuale
            int j = std::uniform_int_distribution<int>(0, m-1)(rng);
            F[j].insert(e);
        }
    }

    // rimuovi insiemi vuoti aggiungendo un elemento casuale
    for (int j = 0; j < m; j++) {
        if (F[j].empty())
            F[j].insert(elem_dist(rng));
    }

    return {universo, F};
}