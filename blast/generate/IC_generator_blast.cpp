#include <fstream>
#include <random>
#include <algorithm>
#include <iostream>

struct Header {
    double time;
    int n;
    int dims;
    int ngas;
    int ndark;
    int nstar;
    int pad;
};

struct Gas {
    float mass;
    float x;
    float y;
    float z;
    float vx;
    float vy;
    float vz;
    float rho;
    float temp;
    float hsmooth;
    float metals;
    float phi;
};

struct Dark {
    float mass;
    float x;
    float y;
    float z;
    float vx;
    float vy;
    float vz;
    float eps;
    float phi;
};

struct Star {
    float mass;
    float x;
    float y;
    float z;
    float vx;
    float vy;
    float vz;
    float metals;
    float tform;
    float eps;
    float phi;
};

void generate(const int N, std::string filename) {
    const double spacing = 1.0 / N;
    std::ofstream file(filename, std::ios::binary);

    // random number generator
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_real_distribution<float> dis(0.1, 0.9);

    // Write header
    Header* header = new Header;
    header->time = 1.0;
    header->n = N*N*N;
    header->dims = 3;
    header->ngas = N*N*N;
    header->ndark = 0;
    header->nstar = 0;
    header->pad = 0;
    file.write(reinterpret_cast<const char*>(header), sizeof(Header));

    // Write gas
    Gas* gas = new Gas[N*N*N];
    for (int x=0; x<N; ++x) {
        for (int y=0; y<N; ++y) {
            for (int z=0; z<N; ++z) {
                int i = x + N * (y + N * z);
                gas[i].mass = 1.0/(N*N*N);
                gas[i].x = (x - 0.5*N + dis(gen)) * spacing;
                gas[i].y = (y - 0.5*N + dis(gen)) * spacing;
                gas[i].z = (z - 0.5*N + dis(gen)) * spacing;
                gas[i].vx = 0.0;
                gas[i].vy = 0.0;
                gas[i].vz = 0.0;
                gas[i].rho = 1.0;
                gas[i].temp = 10;
                gas[i].hsmooth = 0.0;
                gas[i].metals = 0.0;
                gas[i].phi = 0.0;
            }
        }
    }
    file.write(reinterpret_cast<const char*>(gas), sizeof(Gas) * N*N*N);
}

int main(int argc, char** argv) {
    const int N = atoi(argv[1]);
    generate(N, "ic_blast_grid_" + std::to_string(N) + ".tipsy");
    return 0;
}
