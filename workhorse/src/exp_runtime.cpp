#include "exp_runtime.h"
#include "generator.h"
#include "greedy.h"
#include "greedy_hashmap.h"
#include "randomized.h"
#include <iostream>
#include <fstream>
#include <vector>
#include <set>
#include <ctime>

template<typename Func>
double measure_time(Func f) {
    std::clock_t start = std::clock();
    f();
    return double(std::clock() - start) / CLOCKS_PER_SEC;
}

bool is_valid_cover_rt(
    const std::set<int>& universo,
    const std::vector<std::set<int>>& F,
    const std::vector<int>& cover)
{
    std::set<int> covered;
    for (int j : cover)
        for (int e : F[j])
            covered.insert(e);
    return covered == universo;
}

void run_exp_runtime() {

    std::vector<int>    n_vals = {100, 200, 400, 800, 1600, 3200, 6400, 12800, 25600, 51200};
    std::vector<int>    m_vals = {20, 50, 100};
    std::vector<double> p_vals = {0.1, 0.3, 0.5};
    std::vector<int>    seeds  = {42, 123, 7, 31, 999, 17, 53, 77, 101, 200};
    double c = 2.0;

    std::ofstream csv("risultati/workhorse_results.csv");
    csv << "n,m,p,seed,algoritmo,dim_cover,tempo_sec,valid\n";

    for (int n : n_vals) {
        for (int m : m_vals) {
            for (double p : p_vals) {
                for (int seed : seeds) {

                    auto [universo, F] = generate_instance_bernoulli(n, m, p, seed);

                    {
                        std::vector<int> cover;
                        double t = measure_time([&](){ cover = greedy_set_cover(universo, F); });
                        bool valid = is_valid_cover_rt(universo, F, cover);
                        csv << n << "," << m << "," << p << "," << seed
                            << ",Greedy," << cover.size() << "," << t << "," << valid << "\n";
                    }

                    {
                        std::vector<int> cover;
                        double t = measure_time([&](){ cover = greedy_hashmap_setcover(universo, F); });
                        bool valid = is_valid_cover_rt(universo, F, cover);
                        csv << n << "," << m << "," << p << "," << seed
                            << ",GreedyHashMap," << cover.size() << "," << t << "," << valid << "\n";
                    }

                    {
                        std::vector<int> cover;
                        double t = measure_time([&](){ cover = randomized_rounding(universo, F, c, seed); });
                        bool valid = is_valid_cover_rt(universo, F, cover);
                        csv << n << "," << m << "," << p << "," << seed
                            << ",Randomized," << cover.size() << "," << t << "," << valid << "\n";
                    }
                }
                std::cout << "n=" << n << " m=" << m << " p=" << p << " completato\n";
            }
        }
    }

    csv.close();
    std::cout << "Exp runtime completato.\n";
}
