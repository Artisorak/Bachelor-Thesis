import numpy as np

M = 5.27e39
L = 1.85e20
T = 4.24e15
RHO = M/(L**3)
E = 6.78e46

def sedov_solution(t):

  n = 200

  gamma = 5.0 / 3.0

  # Total energy: e*m
  energy = E # 1.0 #/(5./3-1.) #3.81439 #1.0  
  rho1 = RHO # 1.0

  lamda = 1.1527

  nu = 3.0

  gammap1 = gamma + 1
  gammam1 = gamma - 1
  gammam2 = gamma - 2

  nup2 = nu + 2

  alpha2 = -gammam1 / (2 * gammam1 + nu)

  alpha1 = nup2 * gamma / (2 + nu * gammam1) * (2 * nu * (-gammam2) / (gamma * nup2**2) - alpha2)

  alpha3 = nu / (2 * gammam1 + nu)

  alpha4 = alpha1 * nup2 / (-gammam2)

  alpha5 = 2.0 / gammam2



  rho2 = gammap1 / gammam1 * rho1
  r2 = lamda * (energy / rho1)**(1.0 / nup2) * t**(2.0 / nup2)



  V0 = 2 / (nup2 * gamma)
  V1 = 4 / (nup2 * gammap1)

  V = np.linspace(V0, V1, n) #findgen(n) / (n - 1) * (V1 - V0) + V0

  r = r2 * (nup2 * gammap1 / 4 * V)**(-2 / nup2) * \
      (gammap1 / gammam1 *(nup2 * gamma / 2 * V - 1))**(-alpha2) * \
      (nup2 * gammap1 / (nup2 * gammap1 - 2 * (2 + nu * gammam1)) * (1 - (2 + nu * gammam1) / 2 * V))**(-alpha1)

  rho = rho2 * (gammap1 / gammam1 * (nup2 * gamma / 2 * V - 1))**alpha3 * \
        (gammap1 / gammam1 * (1 - nup2 / 2 * V))**alpha5 * \
        (nup2 * gammap1 / (nup2 * gammap1 - 2 * (2 + nu * gammam1)) * (1 - (2 + nu * gammam1) / 2 * V))**alpha4

  r = np.append(r, [r[-1], 0.5*L])
  rho = np.append(rho, [RHO,RHO])

  return r, rho