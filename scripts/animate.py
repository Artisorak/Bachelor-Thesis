#!/usr/bin/env python
import numpy as np
import pandas as pd
from sys import argv,exit
from matplotlib import pyplot as plt
import matplotlib.animation as animation

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

achOutName = argv[1]

skip = 10
nsteps = int(argv[2])
dt = 0.01

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

mode = "density"
if len(argv) > 3:
    mode = argv[3]
print(mode)

if mode == "velocity":
    import colorsys

def animate(i):
    t = dt*i
    print("\nProcessing frame /cluster/scratch/ariess/%s/%s.%s"%(achOutName, achOutName, str(i).zfill(5)))
    try:
        tipsy = open("/cluster/scratch/ariess/%s/%s.%s"%(achOutName, achOutName, str(i).zfill(5)),'rb')
    except:
        print("Error: file not found")
        # ax.set_title('STEP %s'%str(i).zfill(5) + ' TIME {:e}'.format(t*T))
        return

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
    if t < 1.0: t = 1.0

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
    if mode == "temperature":
        gas.sort_values(by=['temp'], ascending=True, inplace=True)
    elif mode == "velocity":
        # add velocity magnitude column
        gas['v'] = np.sqrt(gas['vx']**2 + gas['vy']**2 + gas['vz']**2)
        gas.sort_values(by=['v'], ascending=True, inplace=True)
        # remove velocity magnitude column
        gas.drop(columns=['v'], inplace=True)
    else:
        gas.sort_values(by=['rho'], ascending=True, inplace=True)

    # define color scheme
    if mode == "temperature":
        c = np.log10(gas['temp'])
    elif mode == "velocity":
        # color in HSV, velocity direction on x-y-plane is hue, speed is value
        hue = np.array(np.arctan2(gas['vy'], gas['vx']) / (2*np.pi))
        hue = np.mod(hue, 1)
        value = np.array(np.sqrt(gas['vx']**2 + gas['vy']**2 + gas['vz']**2))
        print(hue, len(hue))
        print(value, len(value))
        c = np.array([colorsys.hsv_to_rgb(hue[j], 1, value[j]) for j in range(len(hue))])
        print(c, len(c))
        c = np.array(['#%02x%02x%02x'%(int(c[j,0]*255), int(c[j,1]*255), int(c[j,2]*255)) for j in range(len(hue))])
        c = c.T
    else:
        c = np.log10(gas['rho'])

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
    ax.set_title('STEP %s'%str(i).zfill(5) + ' TIME {:e}'.format((t-1.0)*T))
    # plt.colorbar()

anim = animation.FuncAnimation(fig, func=animate, frames=nsteps+1)
mp4writer = animation.FFMpegWriter(fps=5)
anim.save('animations/animation_%s_%s.mp4'%(achOutName, mode), writer=mp4writer, dpi=300)

# clear for energy plot
plt.clf()

plt.plot(np.linspace(0, nsteps+1, nsteps+1), rmsvel[1:nsteps+2], label='rms velocity')
plt.legend()
plt.xlabel('step')
# plt.ylabel('energy [J]')
plt.semilogy()
plt.savefig('animations/energy_%s.png'%achOutName, dpi=300)