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
M       = 3.90e34           # code unit mass in kg
L       = 6.17e17           # code unit length in m
T       = 3e14              # code unit time in s
RHO     = M/(L**3)          # code unit density in kg/m^3
gamma   = 1.4               # adiabatic index

left = open("/home/ariess/EULER/cluster/bachelorthesis/NewSPH/pkdgrav3/run/sod_ic_grid_isentrope_left_relaxed1600.tipsy",'rb')
header = np.fromfile(left,dtype=header_type,count=1)
leftheader = dict(zip(header_type.names,header[0]))
gas  = np.fromfile(left,dtype=gas_type,count=leftheader['Ngas'])
leftgas  = pd.DataFrame(gas,columns=gas.dtype.names)
dark = np.fromfile(left,dtype=dark_type,count=leftheader['Ndark'])
leftdark = pd.DataFrame(dark,columns=dark.dtype.names)
star = np.fromfile(left,dtype=star_type,count=leftheader['Nstar'])
star1 = pd.DataFrame(star,columns=star.dtype.names)
left.close()

right = open("/home/ariess/EULER/cluster/bachelorthesis/NewSPH/pkdgrav3/run/sod_ic_grid_isentrope_right_relaxed1600.tipsy",'rb')
header = np.fromfile(right,dtype=header_type,count=1)
rightheader = dict(zip(header_type.names,header[0]))
gas  = np.fromfile(right,dtype=gas_type,count=rightheader['Ngas'])
rightgas  = pd.DataFrame(gas,columns=gas.dtype.names)
dark = np.fromfile(right,dtype=dark_type,count=rightheader['Ndark'])
rightdark = pd.DataFrame(dark,columns=dark.dtype.names)
star = np.fromfile(right,dtype=star_type,count=rightheader['Nstar'])
rightstar = pd.DataFrame(star,columns=star.dtype.names)
right.close()

# move the two boxes, gas1 is for the left half, gas2 for the right half
leftgas['x'] = leftgas['x'] - 0.5
rightgas['x'] = rightgas['x'] + 0.5
leftgas['x'] *= 0.5
leftgas['y'] *= 0.5
leftgas['z'] *= 0.5
rightgas['x'] *= 0.5
rightgas['y'] *= 0.5
rightgas['z'] *= 0.5

# pressure in right half is one 10th of the temperature in the left half
# right now it's one 8th
# we have to scale the temperature in the right half by 8/10
leftc = 10.0*1.0**(1.0-gamma)
leftgas['temp'] = leftc / leftgas['rho']**(1.0-gamma)
rightc = 8.0*1.0**(1.0-gamma)
rightgas['temp'] = rightc / rightgas['rho']**(1.0-gamma)
gas = pd.concat([leftgas,rightgas], ignore_index=True)

header = leftheader

header['Ngas'] = len(gas)
header['Ndark'] = len(dark)
header['Nstar'] = len(star)
header['N'] = header['Ngas'] + header['Ndark'] + header['Nstar']
header['time'] = 1.0

gas['mass'] = [1.0/256/header['Ngas']]*header['Ngas']
gas['hsmooth'] = np.mean(gas['hsmooth'])

print(header)
print(gas)
# print(dark)
# print(star)

with open("sod_ic_grid_isentrope_relaxed1600_combined.txt","w") as f:
    print("HEADER")
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