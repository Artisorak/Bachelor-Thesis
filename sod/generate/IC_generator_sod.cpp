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

void generate(const int Nx, const int Ny, const int Nz, std::string filename) {
    const int N = Nx * Ny * Nz;
    const double spacing = 1.0 / Nx;
    std::ofstream file(filename, std::ios::binary);

    // random number generator
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_real_distribution<float> dis(0.1, 0.9);

    // Write header
    Header* header = new Header;
    header->time = 1.0;
    header->n = N;
    header->dims = 3;
    header->ngas = N;
    header->ndark = 0;
    header->nstar = 0;
    header->pad = 0;
    file.write(reinterpret_cast<const char*>(header), sizeof(Header));

    // Write gas
    Gas* gas = new Gas[N];
    for (int x=0; x<Nx; ++x) {
        for (int y=0; y<Ny; ++y) {
            for (int z=0; z<Nz; ++z) {
                int i = x + Nx * (y + Ny * z);
                gas[i].mass = 1.0/(Nx*Nx*Nx);
                gas[i].x = (x - 0.5*Nx + dis(gen)) * spacing;
                gas[i].y = (y - 0.5*Ny + dis(gen)) * spacing;
                gas[i].z = (z - 0.5*Nz + dis(gen)) * spacing;
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
    file.write(reinterpret_cast<const char*>(gas), sizeof(Gas) * N);
}

int main() {
    const int Nlx = 256;
    const int Nly = 32;
    const int Nlz = 32;
    generate(Nlx, Nly, Nlz, "ic_sod_grid_left_" + std::to_string(Nlx) + "_" + std::to_string(Nly) + "_" + std::to_string(Nlz) + ".tipsy");

    const int Nrx = 128;
    const int Nry = 16;
    const int Nrz = 16;
    generate(Nrx, Nry, Nrz, "ic_sod_grid_right_" + std::to_string(Nrx) + "_" + std::to_string(Nry) + "_" + std::to_string(Nrz) + ".tipsy");
    return 0;
}
