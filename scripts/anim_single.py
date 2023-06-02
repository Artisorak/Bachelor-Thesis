#!/usr/bin/env python
import numpy as np
import pandas as pd
from sys import argv,exit
from matplotlib import pyplot as plt

header_type = np.dtype([('time', '=f8'),('N', '=i4'), ('Dims', '=i4'), ('Ngas', '=i4'), ('Ndark', '=i4'), ('Nstar', '=i4'), ('pad', '=i4')])
gas_type  = np.dtype([('mass','=f4'), ('x', '=f4'),('y', '=f4'),('z', '=f4'), ('vx', '=f4'),('vy', '=f4'),('vz', '=f4'),
                    ('rho','=f4'), ('temp','=f4'), ('hsmooth','=f4'), ('metals','=f4'), ('phi','=f4')])
dark_type = np.dtype([('mass','=f4'), ('x', '=f4'),('y', '=f4'),('z', '=f4'), ('vx', '=f4'),('vy', '=f4'),('vz', '=f4'),
                    ('eps','=f4'), ('phi','=f4')])
star_type  = np.dtype([('mass','=f4'), ('x', '=f4'),('y', '=f4'),('z', '=f4'), ('vx', '=f4'),('vy', '=f4'),('vz', '=f4'),
                    ('metals','=f4'), ('tform','=f4'), ('eps','=f4'), ('phi','=f4')])

projection = "2d"

fig = plt.figure()
if projection == "3d": ax = plt.axes(projection='3d')
else: ax = plt.axes()

skip = 10
nsteps = int(argv[2])
dt = 0.05

achOutName = argv[1]

kB = 1.38064852e-23 # Boltzmann constant in SI units
u = 1.660538921e-27 # atomic mass unit in kg
M = 3.90e34         # code unit mass in kg
L = 6.17e17         # code unit length in m
T = 3e14            # code unit time in s
RHO = M/(L**3)      # code unit density in kg/m^3

blast_mode = False    
if "blast" in achOutName:
    blast_mode = True
    dt = 0.0005
    M = 5.27e39
    L = 1.85e20
    T = 4.24e15
    RHO = M/(L**3)
if achOutName == "relax_blast": dt = 0.1
print(blast_mode)

rmsvel = []

mode = None
if len(argv) > 2:
    mode = argv[2]

print("\nProcessing frame /home/ariess/EULER/scratch/%s/%s.%s"%(achOutName, achOutName, str(nsteps).zfill(5)))
try:
    tipsy = open("/home/ariess/EULER/scratch/%s/%s.%s"%(achOutName, achOutName, str(nsteps).zfill(5)),'rb')
except:
    print("Error: file not found")
    # ax.set_title('STEP %s'%str(i).zfill(5) + ' TIME {:e}'.format(t*T))
    exit(1)

print("Reading file")
header = np.fromfile(tipsy,dtype=header_type,count=1)
header = dict(zip(header_type.names,header[0]))
if projection == "3d":
    header['N']     //= skip
    header['Ngas']  //= skip
    header['Ndark'] //= skip
    header['Nstar'] //= skip
gas  = np.fromfile(tipsy, dtype =  gas_type, count=header['Ngas'])
gas  = pd.DataFrame(gas,  columns = gas.dtype.names)
dark = np.fromfile(tipsy, dtype = dark_type, count=header['Ndark'])
dark = pd.DataFrame(dark, columns = dark.dtype.names)
star = np.fromfile(tipsy, dtype = star_type, count=header['Nstar'])
star = pd.DataFrame(star, columns = star.dtype.names)
tipsy.close()

t = header['time']

# get slice of particles from z=-0.1 to z=0.1
if projection == "2d":
    gas  =  gas[( gas['z'] > -0.1) & ( gas['z'] < 0.1)]
    dark = dark[(dark['z'] > -0.1) & (dark['z'] < 0.1)]
    star = star[(star['z'] > -0.1) & (star['z'] < 0.1)]

# rms velocity
rmsvel.append(np.sqrt(np.mean(gas['vx']**2 + gas['vy']**2 + gas['vz']**2)))

print("mean velocity:       %f"%(np.mean(np.sqrt(gas['vx']**2 + gas['vy']**2 + gas['vz']**2))))
print("mean density:        %f"%(np.mean(gas['rho'])))
print("mean temperature:    %f"%(np.mean(gas['temp'])))

print("Plotting")
ax.cla()

# sort gas particles by density so that those with highest density are plotted on top
if mode != "velocity":
    gas.sort_values(by=['rho'], ascending=True, inplace=True)
else:
    # add velocity magnitude column
    gas['v'] = np.sqrt(gas['vx']**2 + gas['vy']**2 + gas['vz']**2)
    gas.sort_values(by=['v'], ascending=True, inplace=True)
    # remove velocity magnitude column
    gas.drop(columns=['v'], inplace=True)

# define color scheme
c = gas['rho']*RHO # np.log10(gas['rho']*RHO)
if mode == "velocity":
    # color in HSV, velocity direction on x-y-plane is hue, speed is value
    hue = np.array(np.arctan2(gas['vy'], gas['vx']) / (2*np.pi))
    hue = np.mod(hue, 1)
    value = np.array(np.sqrt(gas['vx']**2 + gas['vy']**2 + gas['vz']**2))
    print(hue, len(hue))
    print(value, len(value))
    import colorsys
    c = np.array([colorsys.hsv_to_rgb(hue[i], 1, value[i]) for i in range(len(hue))])
    print(c, len(c))
    c = np.array(['#%02x%02x%02x'%(int(c[i,0]*255), int(c[i,1]*255), int(c[i,2]*255)) for i in range(len(hue))])
    c = c.T
    del colorsys

# plot particles
if projection == "3d":
    ax.scatter( gas['x']*L,    gas['y']*L,   gas['z']*L,  s=0.5,  edgecolors="none", c=c)
    ax.scatter(dark['x']*L,   dark['y']*L,  dark['z']*L,  s=0.5,  edgecolors="none", c='black')
    ax.scatter(star['x']*L,   star['y']*L,  star['z']*L,  s=0.5,  edgecolors="none", c='red')
else:
    ax.scatter( gas['x']*L,    gas['y']*L,  s=0.5,  edgecolors="none", c=c)
    ax.scatter(dark['x']*L,   dark['y']*L,  s=0.5,  edgecolors="none", c='black')
    ax.scatter(star['x']*L,   star['y']*L,  s=0.5,  edgecolors="none", c='red')
ax.set_xlim(-0.5*L, 0.5*L)
ax.set_ylim(-0.5*L, 0.5*L)
ax.set_xlabel(r'x [$m$]')
ax.set_ylabel(r'y [$m$]')
if projection == "3d":
    ax.set_zlim(-0.5*L, 0.5*L)
    ax.set_zlabel(r'z [$m$]')
ax.axis('equal')
ax.set_title('STEP %s'%str(nsteps).zfill(5) + ' TIME {:e}s'.format((t-1.0)*T))
# add colorbar
plt.colorbar(ax.collections[0], ax=ax, label=r'$\rho$ [$kg/m^3$]')
plt.savefig("anim_%s_%i.png"%(achOutName, nsteps), dpi=300)