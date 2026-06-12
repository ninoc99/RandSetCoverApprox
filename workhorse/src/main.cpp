#include <iostream>
#include <string>
#include "exp_runtime.h"
#include "exp_bottleneck.h"

int main(int argc, char* argv[]) {

    if (argc < 2) {
        std::cout << "Usage: ./setcover <experiment>\n";
        std::cout << "  all        -- esegui tutti gli esperimenti\n";
        std::cout << "  runtime    -- runtime, qualita', doubling\n";
        std::cout << "  bottleneck -- bottleneck randomized rounding\n";
        return 1;
    }

    std::string exp = argv[1];

    if (exp == "runtime" || exp == "all")
        run_exp_runtime();

    if (exp == "bottleneck" || exp == "all")
        run_exp_bottleneck();

    if (exp != "runtime" && exp != "bottleneck" && exp != "all") {
        std::cout << "Esperimento non riconosciuto: " << exp << "\n";
        return 1;
    }

    return 0;
}
