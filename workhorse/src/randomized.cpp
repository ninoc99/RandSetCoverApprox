#include "randomized.h"
#include <glpk.h>
#include <vector>
#include <set>
#include <cmath>
#include <random>

std::vector<int> randomized_rounding(
    const std::set<int>& universo,
    const std::vector<std::set<int>>& F,
    double c,
    int seed)
{
    int n = universo.size();
    int m = F.size();
    int t = (int)std::ceil(c * std::log((double)n));

    // ── fase 1: risolvi LP con GLPK ──────────────────────────

    glp_prob* lp = glp_create_prob();
    glp_set_obj_dir(lp, GLP_MIN);

    // silenzia output GLPK
    glp_smcp parm;
    glp_init_smcp(&parm);
    parm.msg_lev = GLP_MSG_OFF;

    // variabili: x_j per ogni insieme S_j, bounds [0,1]
    glp_add_cols(lp, m);
    for (int j = 1; j <= m; j++) {
        glp_set_col_bnds(lp, j, GLP_DB, 0.0, 1.0);
        glp_set_obj_coef(lp, j, 1.0);
    }

    // vincoli: per ogni elemento e, sum_{j: e in S_j} x_j >= 1
    // costruiamo la lista degli elementi nell'ordine del set
    std::vector<int> elems(universo.begin(), universo.end());
    glp_add_rows(lp, n);
    for (int i = 0; i < n; i++)
        glp_set_row_bnds(lp, i+1, GLP_LO, 1.0, 0.0);

    // popola la matrice dei vincoli
    // GLPK usa indici 1-based
    for (int i = 0; i < n; i++) {
        int e = elems[i];
        std::vector<int>    ind;
        std::vector<double> val;
        ind.push_back(0); // placeholder indice 0 (GLPK ignora ind[0])
        val.push_back(0.0);
        for (int j = 0; j < m; j++) {
            if (F[j].count(e)) {
                ind.push_back(j+1);
                val.push_back(1.0);
            }
        }
        glp_set_mat_row(lp, i+1,
                        (int)ind.size()-1,
                        ind.data(),
                        val.data());
    }

    glp_simplex(lp, &parm);

    // estrai soluzione LP
    std::vector<double> x_hat(m);
    for (int j = 0; j < m; j++)
        x_hat[j] = glp_get_col_prim(lp, j+1);

    glp_delete_prob(lp);

    // ── fase 2: t round di rounding randomizzato ─────────────

    std::mt19937 rng(seed);
    std::uniform_real_distribution<double> dist(0.0, 1.0);

    std::set<int> selected_set;
    for (int r = 0; r < t; r++)
        for (int j = 0; j < m; j++)
            if (dist(rng) < x_hat[j])
                selected_set.insert(j);

    return std::vector<int>(selected_set.begin(), selected_set.end());
}