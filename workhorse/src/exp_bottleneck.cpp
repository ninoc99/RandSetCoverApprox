#include "exp_bottleneck.h"
#include "generator.h"
#include <iostream>
#include <fstream>
#include <vector>
#include <set>
#include <random>
#include <ctime>
#include <cmath>
#include <glpk.h>

void run_exp_bottleneck() {

    std::vector<int>    n_vals = {100, 200, 400, 800, 1600, 3200, 6400, 12800};
    std::vector<int>    m_vals = {20, 50, 100};
    double p = 0.3;
    std::vector<int>    seeds  = {42, 123, 7, 31, 999};
    double c = 2.0;

    std::ofstream csv("risultati/bottleneck_results.csv");
    csv << "n,m,p,seed,t_lp,t_round,t_verifica,t_totale\n";

    for (int n : n_vals) {
        for (int m : m_vals) {
            for (int seed : seeds) {

                auto [universo, F] = generate_instance_bernoulli(n, m, p, seed);
                int t = (int)std::ceil(c * std::log((double)n));

                // fase 1: LP
                std::clock_t t0 = std::clock();

                glp_prob* lp = glp_create_prob();
                glp_set_obj_dir(lp, GLP_MIN);
                glp_smcp parm;
                glp_init_smcp(&parm);
                parm.msg_lev = GLP_MSG_OFF;

                glp_add_cols(lp, m);
                for (int j = 1; j <= m; j++) {
                    glp_set_col_bnds(lp, j, GLP_DB, 0.0, 1.0);
                    glp_set_obj_coef(lp, j, 1.0);
                }

                std::vector<int> elems(universo.begin(), universo.end());
                glp_add_rows(lp, n);
                for (int i = 0; i < n; i++)
                    glp_set_row_bnds(lp, i+1, GLP_LO, 1.0, 0.0);

                for (int i = 0; i < n; i++) {
                    int e = elems[i];
                    std::vector<int>    ind = {0};
                    std::vector<double> val = {0.0};
                    for (int j = 0; j < m; j++)
                        if (F[j].count(e)) { ind.push_back(j+1); val.push_back(1.0); }
                    glp_set_mat_row(lp, i+1, (int)ind.size()-1, ind.data(), val.data());
                }

                glp_simplex(lp, &parm);

                std::vector<double> x_hat(m);
                for (int j = 0; j < m; j++)
                    x_hat[j] = glp_get_col_prim(lp, j+1);
                glp_delete_prob(lp);

                double t_lp = double(std::clock() - t0) / CLOCKS_PER_SEC;

                // fase 2: rounding
                t0 = std::clock();
                std::mt19937 rng(seed);
                std::uniform_real_distribution<double> dist(0.0, 1.0);
                std::set<int> selected_set;
                for (int r = 0; r < t; r++)
                    for (int j = 0; j < m; j++)
                        if (dist(rng) < x_hat[j])
                            selected_set.insert(j);
                double t_round = double(std::clock() - t0) / CLOCKS_PER_SEC;

                // fase 3: verifica
                t0 = std::clock();
                std::set<int> covered;
                for (int j : selected_set)
                    for (int e : F[j])
                        covered.insert(e);
                double t_verifica = double(std::clock() - t0) / CLOCKS_PER_SEC;

                double t_totale = t_lp + t_round + t_verifica;

                csv << n << "," << m << "," << p << "," << seed << ","
                    << t_lp << "," << t_round << "," << t_verifica << ","
                    << t_totale << "\n";
            }
            std::cout << "n=" << n << " m=" << m << " completato\n";
        }
    }

    csv.close();
    std::cout << "Exp bottleneck completato.\n";
}
