import numpy as np
import pandas as pd
from sys import argv,exit
from matplotlib import pyplot as plt
import sod
import sedov_solution

header_type = np.dtype([('time', '=f8'),('N', '=i4'), ('Dims', '=i4'), ('Ngas', '=i4'), ('Ndark', '=i4'), ('Nstar', '=i4'), ('pad', '=i4')])
gas_type  = np.dtype([('mass','=f4'), ('x', '=f4'),('y', '=f4'),('z', '=f4'), ('vx', '=f4'),('vy', '=f4'),('vz', '=f4'),
                    ('rho','=f4'), ('temp','=f4'), ('hsmooth','=f4'), ('metals','=f4'), ('phi','=f4')])
dark_type = np.dtype([('mass','=f4'), ('x', '=f4'),('y', '=f4'),('z', '=f4'), ('vx', '=f4'),('vy', '=f4'),('vz', '=f4'),
                    ('eps','=f4'), ('phi','=f4')])
star_type  = np.dtype([('mass','=f4'), ('x', '=f4'),('y', '=f4'),('z', '=f4'), ('vx', '=f4'),('vy', '=f4'),('vz', '=f4'),
                    ('metals','=f4'), ('tform','=f4'), ('eps','=f4'), ('phi','=f4')])

fig = plt.figure()
ax = plt.axes()

skip = 10
dt = 0.01

kB = 1.38064852e-23 # Boltzmann constant in SI units
u = 1.660538921e-27 # atomic mass unit in kg
M = 3.90e34         # code unit mass in kg
L = 6.17e17         # code unit length in m
T = 3e14            # code unit time in s
RHO = M/(L**3)      # code unit density in kg/m^3

achOutName = argv[1]

blast_mode = False    
if "blast" in achOutName:
    blast_mode = True
    dt = 0.0005
    M = 5.27e39
    L = 1.85e20
    T = 4.24e15
    RHO = M/(L**3)
print(blast_mode)

if len(argv) < 3:
    mode = 'density'
else:
    mode = argv[2]
print(mode)

mean = True

code_units = False
if code_units:
    M = 1
    L = 1
    T = 1
    RHO = 1

def plot(i):
    t = 1.0 + dt*i
    print("")
    print("Processing frame /home/ariess/EULER/scratch/%s/%s.%s"%(achOutName, achOutName, str(i).zfill(5)))
    try:
        tipsy = open("/home/ariess/EULER/scratch/%s/%s.%s"%(achOutName, achOutName, str(i).zfill(5)),'rb')
    except:
        print("Error: file not found")
        # ax.set_title('STEP %s'%str(i).zfill(5) + ' TIME {:e}s'.format((t-1.0)*T))
        return

    print("Reading file")
    header = np.fromfile(tipsy,dtype=header_type,count=1)
    header = dict(zip(header_type.names,header[0]))
    # header['N']     //= skip
    # header['Ngas']  //= skip
    # header['Ndark'] //= skip
    # header['Nstar'] //= skip
    gas  = np.fromfile(tipsy, dtype =  gas_type, count=header['Ngas'])
    gas  = pd.DataFrame(gas,  columns = gas.dtype.names)
    dark = np.fromfile(tipsy, dtype = dark_type, count=header['Ndark'])
    dark = pd.DataFrame(dark, columns = dark.dtype.names)
    star = np.fromfile(tipsy, dtype = star_type, count=header['Nstar'])
    star = pd.DataFrame(star, columns = star.dtype.names)
    tipsy.close()

    t = header['time']
    if t < 1.0: t = 1.0

    ax.cla()
    # sort gas particles by density so that those with highest density are plotted on top
    gas.sort_values(by=['rho'], ascending=True, inplace=True)

    print("Plotting")

    if blast_mode:
        gas['r'] = np.sqrt(gas['x']**2 + gas['y']**2 + gas['z']**2)
        if mode == "density":
            # plot particle x-position vs. density
            ax.scatter(gas['r']*L, gas['rho']*RHO, s=0.5, edgecolors="none")
        elif mode == "pressure":
            # plot particle x-position vs. pressure
            ax.scatter(gas['r']*L, gas['temp']*gas['rho']*kB/u*RHO, s=0.5, edgecolors="none")
        else:
            # plot particle x-position vs. density
            ax.scatter(gas['r']*L, gas['rho']*RHO, s=0.5, edgecolors="none")
        # plot position of blast radius according to analytic solution
        # ax.scatter([blast.r((t-1.0)*T)], [blast.RHO], s=10, c='r', label='analytic blast radius')
        if mean:
            # plot mean density or pressure
            meanrho = np.zeros(500)
            meanPr = np.zeros(500)
            dx = 0.5/len(meanrho)
            for j in range(len(meanrho)):
                meanrho[j] = np.mean(gas[(dx*j < gas['r']) & (gas['r'] < dx*(j+1))]['rho'])
                meanPr[j] = np.mean(gas[(dx*j < gas['r']) & (gas['r'] < dx*(j+1))]['temp']) * meanrho[j]
            if mode == "density":
                ax.plot(np.linspace(dx/2, 0.5-dx/2, len(meanrho))*L, meanrho*RHO, 'r-', linewidth=1, label=r'mean density')
            elif mode == "pressure":
                ax.plot(np.linspace(dx/2, 0.5-dx/2, len(meanPr))*L, meanPr*kB/u*RHO, 'r-', linewidth=1, label=r'mean pressure')
            else:
                ax.plot(np.linspace(dx/2, 0.5-dx/2, len(meanrho))*L, meanrho*RHO, 'r-', linewidth=1, label=r'mean density')
        # plot analytic solution for blast radius
        ar, arho = sedov_solution.sedov_solution((t-1.0)*T)
        ax.plot(ar, arho, 'k-', linewidth=0.75, label='analytic density')
    else:
        # plot particle x-position vs. density per default, or vs. pressure if mode == "pressure"
        if mode == "density":
            ax.scatter(gas['x']*L, gas['rho']*RHO, s=0.5, edgecolors="none")
        elif mode == "pressure":
            ax.scatter(gas['x']*L, gas['temp']*gas['rho']*kB/u*RHO, s=0.5, edgecolors="none")
        else:
            ax.scatter(gas['x']*L, gas['rho']*RHO, s=0.5, edgecolors="none")
        
        if mean:
            # plot mean density or pressure
            meanrho = np.zeros(1000)
            meanPr = np.zeros(len(meanrho))
            dx = 1.0/len(meanrho)
            for j in range(len(meanrho)):
                meanrho[j] = np.mean(gas[(-0.5 + dx*j < gas['x']) & (gas['x'] < -0.5 + dx*(j+1))]['rho'])
                meanPr[j] = np.mean(gas[(-0.5 + dx*j < gas['x']) & (gas['x'] < -0.5 + dx*(j+1))]['temp']) * meanrho[j]
            if mode == "density":
                ax.plot(np.linspace(-0.5+dx/2, 0.5-dx/2, len(meanrho))*L, meanrho*RHO, 'r-', linewidth=1, label=r'mean density')
            elif mode == "pressure":
                ax.plot(np.linspace(-0.5+dx/2, 0.5-dx/2, len(meanPr))*L, meanPr*kB/u*RHO, 'r-', linewidth=1, label=r'mean pressure')
            else:
                ax.plot(np.linspace(-0.5+dx/2, 0.5-dx/2, len(meanrho))*L, meanrho*RHO, 'r-', linewidth=1, label=r'mean density')
        
        # analytic solution for Sod shock tube
        if "sod" in achOutName and not code_units:
            print("Computing analytic solution for time %f"%(t - 1.0))
            (xgrid, PrE, uE, rhoE, machE, entropy_E) = sod.sod((t - 1.0)*T)
            if mode == "density":
                ax.plot(xgrid[0,:], rhoE[0,:], 'k-', linewidth=1, label=r'analytic density')
                print("Simulation:")
                print(meanrho*RHO)
                print("Analytic:")
                print(rhoE[0,:])
            elif mode == "pressure":
                ax.plot(xgrid[0,:], PrE[0,:], 'k-', linewidth=1, label=r'analytic pressure')
                print("Simulation:")
                print(meanPr*kB/u*RHO)
                print("Analytic:")
                print(PrE)

    if blast_mode:
        ax.set_xlim(0.0, 0.5*L)
    elif "sod"in achOutName and not code_units:
        ax.set_xlim(-0.25*L, 0.25*L)
    else:
        ax.set_xlim(-0.5*L, 0.5*L)
    if code_units:
        ax.set_xlabel(r'x [$L$]')
    else:
        ax.set_xlabel(r'x [$m$]')

    if mode == "density":
        if blast_mode:
            ax.set_ylim(0.0, 5*RHO)
        else:
            ax.set_ylim(0.0, 2*RHO)
        if code_units:
            ax.set_ylabel(r'density [$M/L^3$]')
        else:
            ax.set_ylabel(r'density [$kg/m^3$]')
    elif mode == "pressure":
        ax.set_ylim(0.0, 2*10*kB/u*RHO)
        if code_units:
            ax.set_ylabel(r'pressure [$M/L/T^2$]')
        else:
            ax.set_ylabel(r'pressure [$Pa$]')
    else:
        ax.set_ylim(0.0, 2*RHO)
        if code_units:
            ax.set_ylabel(r'density [$M/L^3$]')
        else:
            ax.set_ylabel(r'density [$kg/m^3$]')
    
    ax.legend(loc='upper right')
    if not code_units:
        ax.set_title('STEP %s'%str(i).zfill(5) + ' TIME {:e}s'.format((t-1.0)*T))

i = int(argv[3])
plot(i)
plt.savefig("plot_%s_%s_%i.png"%(achOutName, mode, i), dpi=300)
plt.show()