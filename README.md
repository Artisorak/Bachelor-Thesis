# Bachelor Thesis

This repository contains my bachelor thesis "A Test Suite for SPH Codes" and the programs I wrote for this project to generate the ICs and to plot the results, along with the final parameter files and initial conditions of the simulations. 

Two types of tests were performed, the Sod shock tube and the Sedov blast wave. This repository only contains the files for the final versions of the tests, and nothing for the tests that did not work well, unless this is requested later. 

## Scripts

This folder contains python programs that can be used to generate ICs or to make plots and animations. When I wrote the code, I did not expect it to be run by other people, so the usage is not very intuitive. Also, the files were not used from within this repository so the paths to other files may have to be changed. 

Usage: `python3 <script> <achOutName> <mode> <steps>`

The shell scripts starting with `run_` are used to run the simulations. They are supposed to be used on Euler, and the paths to the files will have to be changed.

## Sod Shock Tube 

To create the ICs for the Sod Shock Tube test, the two regions of different densities were relaxed separately and then combined into a long tube. 

- `generate` contains everything needed to create the ICs for the relaxation and for the Sod shock tube test.

- `relax` contains everything needed to relax the two regions.

- `run` contains everything needed to run the Sod shock tube test.

- `plots` contains all plots related to the Sod shock tube used in the thesis, and additional animations of the Sod shock tube. 

## Sedov Blast Wave

In the Sedov blast wave test, the energy of a supernova is injected into a small volume in the domain. This was implemented in two ways; First by giving the energy to the particles inside a ball, and second by giving the energy to a single particle. 

- `generate` contains everything needed to create the ICs for the relaxation and for the Sedov blast wave test.

- `relax` contains everything needed to relax the particles. 

- `run` contains everything needed to run the Sedov blast wave test.

- `plots` contains all plots related to the Sedov blast wave used in the thesis, and additional animations of the Sedov bast wave. 
