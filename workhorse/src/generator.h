#pragma once
#include <vector>
#include <set>

// Genera un'istanza Bernoulli per Set Cover
// n: dimensione universo
// m: numero di insiemi
// p: probabilità di inclusione
// seed: seme per riproducibilità
// Ritorna: pair(universo, famiglia di insiemi)
std::pair<std::set<int>, std::vector<std::set<int>>>
generate_instance_bernoulli(int n, int m, double p, int seed);