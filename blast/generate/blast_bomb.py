#!/usr/bin/env python
import numpy as np
import pandas as pd
from sys import argv,exit
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

header_type = np.dtype([('time', '=f8'),('N', '=i4'), ('Dims', '=i4'), ('Ngas', '=i4'), ('Ndark', '=i4'), ('Nstar', '=i4'), ('pad', '=i4')])
gas_type  = np.dtype([('mass','=f4'), ('x', '=f4'),('y', '=f4'),('z', '=f4'), ('vx', '=f4'),('vy', '=f4'),('vz', '=f4'),
                    ('rho','=f4'), ('temp','=f4'), ('hsmooth','=f4'), ('metals','=f4'), ('phi','=f4')])
dark_type = np.dtype([('mass','=f4'), ('x', '=f4'),('y', '=f4'),('z', '=f4'), ('vx', '=f4'),('vy', '=f4'),('vz', '=f4'),
                    ('eps','=f4'), ('phi','=f4')])
star_type  = np.dtype([('mass','=f4'), ('x', '=f4'),('y', '=f4'),('z', '=f4'), ('vx', '=f4'),('vy', '=f4'),('vz', '=f4'),
                    ('metals','=f4'), ('tform','=f4'), ('eps','=f4'), ('phi','=f4')])

kB      = 1.38064852e-23    # Boltzmann constant in SI units
u       = 1.660538921e-27   # atomic mass unit in kg
M       = 5.27e39           # code unit mass in kg
L       = 1.85e20           # code unit length in m
T       = 4.24e15           # code unit time in s
RHO     = M/(L**3)          # code unit density in kg/m^3
gamma   = 5.0/3.0           # adiabatic index

tipsy = open("/home/ariess/EULER/cluster/bachelorthesis/NewSPH/pkdgrav3/run/blast_ic_grid_isentrope_relaxed1600.tipsy",'rb')
header = np.fromfile(tipsy,dtype=header_type,count=1)
header = dict(zip(header_type.names,header[0]))
gas  = np.fromfile(tipsy,dtype=gas_type,count=header['Ngas'])
gas  = pd.DataFrame(gas,columns=gas.dtype.names)
dark = np.fromfile(tipsy,dtype=dark_type,count=header['Ndark'])
dark = pd.DataFrame(dark,columns=dark.dtype.names)
star = np.fromfile(tipsy,dtype=star_type,count=header['Nstar'])
star = pd.DataFrame(star,columns=star.dtype.names)
tipsy.close()

# move particles onto isentrope
c = 10.0*1.0**(1.0-gamma)
gas['temp'] = c / gas['rho']**(1.0-gamma)

# Energy of a supernova in SI units
E = 6.78e46
# E = 1.0e36
indices = []
print("placing bomb")
print(argv[1])
# if energy should be distributed in a ball or given to a single particle
ball = (argv[1] == "ball") # False
if ball:
    for i in range(len(gas)):
        r2 = gas['x'][i]**2 + gas['y'][i]**2 + gas['z'][i]**2
        if r2 < 0.02**2:
            indices.append(i)
    # temperature of the ball
    Ti = E/(3.0/2.0*kB/u*len(indices)*gas['mass'][i]*M)
    for i in indices:
        # distribute the energy of the supernova among the particles in the ball and set their temperature 
        gas['temp'][i] = Ti
    print(str(len(indices)) + " particles are in the ball, each with a temperature of " + str(Ti)) # 56 particles are in the ball, each with a temperature of 3.2567e9 K
else:
    # get particle closes to origin
    i = np.argmin(gas['x']**2 + gas['y']**2 + gas['z']**2)
    Ti = E/(3.0/2.0*kB/u*gas['mass'][i]*M)
    gas['temp'][i] = Ti
    print("particle closest to the origin now has a temperature of " + str(Ti))

header['Ngas'] = len(gas)
header['Ndark'] = len(dark)
header['Nstar'] = len(star)
header['N'] = header['Ngas'] + header['Ndark'] + header['Nstar']
header['time'] = 1.0
gas['mass'] = [1.0/header['Ngas']]*header['Ngas']
hsmooth = np.mean(gas['hsmooth'])
gas['hsmooth'] = hsmooth

print(header)
print(gas)
# print(dark)
# print(star)

with open("blast_ic_grid_isentrope_relaxed1600_bomb_%s.txt"%("ball" if ball else "part"),"w") as f:
    f.write(" %f " % ( header['time']))
    f.write(" %d " % ( header['N']))
    f.write(" %d " % ( header['Dims']))
    f.write(" %d " % ( header['Ngas']))
    f.write(" %d " % ( header['Ndark']))
    f.write(" %d " % ( header['Nstar']))
    f.write(" %d " % ( header['pad']))
    f.write("\n")
    for i in range(0, len(gas)):
        for name in gas.columns:
            f.write(" {:e} ".format(gas[name][i]))
        f.write("\n")