CXX      = clang++
CXXFLAGS = -O2 -std=c++17 -Wall -I/opt/homebrew/include
LDFLAGS  = -L/opt/homebrew/lib -lglpk

SRC = src/main.cpp src/generator.cpp src/greedy.cpp src/greedy_hashmap.cpp src/randomized.cpp src/exp_runtime.cpp src/exp_bottleneck.cpp

TARGET = setcover

$(TARGET): $(SRC)
	$(CXX) $(CXXFLAGS) $(SRC) $(LDFLAGS) -o $(TARGET)

clean:
	rm -f $(TARGET)
