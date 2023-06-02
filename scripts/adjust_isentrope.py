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

# kB      = 1.38064852e-23    # Boltzmann constant in SI units
# u       = 1.660538921e-27   # atomic mass unit in kg
# M       = 3.90e34           # code unit mass in kg
# L       = 6.17e17           # code unit length in m
# T       = 3e14              # code unit time in s
# RHO     = M/(L**3)          # code unit density in kg/m^3
# gamma   = 1.4               # adiabatic index

gamma = float(argv[2])
print("gamma: %f"%gamma)

tipsy = open(str(argv[1]),'rb')
header = np.fromfile(tipsy,dtype=header_type,count=1)
header = dict(zip(header_type.names,header[0]))
gas  = np.fromfile(tipsy,dtype=gas_type,count=header['Ngas'])
gas  = pd.DataFrame(gas,columns=gas.dtype.names)
tipsy.close()

print("adjusting temperature")
c = 10.0*1.0**(1.0-gamma) # constant = temperature * density^(1-gamma)
gas['temp'] = c / gas['rho']**(1.0-gamma)

print("standard deviation of isentrope: %f"%np.std(gas['temp'] * gas['rho']**(1.0-gamma)))

hsmooth = np.mean(gas['hsmooth'])
gas['hsmooth'] = hsmooth

print(header)
print(gas)
print("mean density: %f"%np.mean(gas['rho']))
print("mean temperature: %f"%np.mean(gas['temp']))

with open("%s_adjusted_isentrope.txt"%argv[1],"w") as f:
    f.write(" %f " %(header['time']))
    f.write(" %d " %(header['N']))
    f.write(" %d " %(header['Dims']))
    f.write(" %d " %(header['Ngas']))
    f.write(" %d " %(header['Ndark']))
    f.write(" %d " %(header['Nstar']))
    f.write(" %d " %(header['pad']))
    f.write("\n")
    for i in range(0, len(gas)):
        for name in gas.columns:
            f.write(" {:e} ".format(gas[name][i]))
        f.write("\n")