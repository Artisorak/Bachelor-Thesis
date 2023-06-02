#include <fstream>
#include <random>
#include <algorithm>
#include <cassert>
#include <iostream>

#define NGRID   256
#define N       (NGRID*NGRID*NGRID)
#define NGAS    (NGRID*NGRID*NGRID)
#define NDARK   0
#define NSTAR   0

struct Header {
    double time = 1;
    int n = N;
    int dims = 3;
    int ngas = NGAS;
    int ndark = NDARK;
    int nstar = NSTAR;
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

int main() {
    assert(N == NGAS + NDARK + NSTAR);

    std::ofstream file("pkdgrav3/run/ics.tipsy", std::ios::binary);

    // random number generator
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_real_distribution<float> dis(0.0, 1.0);

    // Write header
    Header* header = new Header;
    file.write(reinterpret_cast<const char*>(header), sizeof(Header));

    // Write gas
    Gas* gas = new Gas[NGAS];
    for (unsigned i=0; i<NGAS; ++i) {
        gas[i].mass     = 1.0/(NGAS);
        gas[i].x        = (i % NGRID            + dis(gen)) / NGRID - 0.5;
        gas[i].y        = ((i / NGRID) % NGRID  + dis(gen)) / NGRID - 0.5;
        gas[i].z        = (i / (NGRID * NGRID)  + dis(gen)) / NGRID - 0.5;
        gas[i].vx       = 0.0;
        gas[i].vy       = 0.0;
        gas[i].vz       = 0.0;
        gas[i].rho      = 1.0;
        gas[i].temp     = 10.0;
        gas[i].hsmooth  = 0.0;
        gas[i].metals   = 0.0;
        gas[i].phi      = 0.0;
    }
    file.write(reinterpret_cast<const char*>(gas), sizeof(Gas) * NGAS);

    // Write dark
    Dark* dark = new Dark[NDARK];
    for (unsigned i=0; i<NDARK; ++i) {
        dark[i].mass    = 1.0/(NDARK);
        dark[i].x       = dis(gen) - 0.5;
        dark[i].y       = dis(gen) - 0.5;
        dark[i].z       = dis(gen) - 0.5;
        dark[i].vx      = 0;
        dark[i].vy      = 0;
        dark[i].vz      = 0;
        dark[i].eps     = 1.0/50/NGRID;
        dark[i].phi     = 0.0;
    }
    file.write(reinterpret_cast<const char*>(dark), sizeof(Dark) * NDARK);

    // Write star
    Star* star = new Star[NSTAR];
    for (unsigned i=0; i<NSTAR; ++i) {
        star[i].mass    = 1.0/(NSTAR);
        star[i].x       = dis(gen) - 0.5;
        star[i].y       = dis(gen) - 0.5;
        star[i].z       = dis(gen) - 0.5;
        star[i].vx      = 0;
        star[i].vy      = 0;
        star[i].vz      = 0;
        star[i].metals  = 0.0;
        star[i].tform   = 0.0;
        star[i].eps     = 1.0/50/NGRID;
        star[i].phi     = 0.0;
    }
    file.write(reinterpret_cast<const char*>(star), sizeof(Star) * NSTAR);

    return 0;
}
