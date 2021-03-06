#!/bin/env python

# *****************************************************************************
# Test Description: 
# 1D heat conduction with constant thermal conductivity in time and space, with 
# a complex initial temperature distribution and steady no heat flux boundary
# conditions at left and right ends of the beam. Solution is evaluated at 
# t=0.05 day and t=0.1 day.
#
# Kolditz, et al. (2015) Thermo-Hydro-Mechanical-Chemical Processes in 
# Fractured Porous Media: Modelling and Benchmarking, Closed Form Solutions,
# Springer International Publishing, Switzerland.
# Section 2.1.8, pg.21
# "A Transient 1D Temperature Distribution, Non-Zero Initial Temperature,
# Boundary Conditions of 1st and 2nd Kind"
# With some modification of the parameter values given in Kolditz (2015)
#
# Author: Jenn Frederick
# Date: 07/13/2016
# *****************************************************************************
#
# Domain
# ------
# 100x1x1 hexahedral elements
# 1x1x1 meter elements
# L = 100 m, domain x = 0:L
# Only beam T2 is considered
#
# Parameters
# ----------
# 0.5787037 W/m-C thermal conductivity everywhere, constant in time
# 0.01 J/kg-C heat capacity everywhere, constant in time
# 2000 kg/m^3 density everywhere, constant in time
#
# Initial Conditions
# ------------------
# At t=0, T=1C*f(x) everywhere
# f(x) =
# 0C for [0 <= x <= L/10]
# ((10/3L)x - (1/3))C for [L/10 <= x <= 4L/10]
# 1C for [4L/10 <= x <= 6L/10]
# (3 - (10/3L)x)C for [6L/10 <= x <= 9L/10]
# 0C for [9L/10 <= x <= L]
#
# Boundary Conditions
# -------------------
# At x=0m, q = 0
# At x=L=100m, q=0
#
# Time Stepping
# -------------
# Maximum timestep enforced: 0.01 day
#
# Simulation Time
# ---------------
# Simulations runs for 0.5 days
# Solution at t=0.05 day and t=0.10 day evaluated
# 
# Solution (time-dependent)
# -------------------------
# T2(x,t) = 0.5 + sum_n=1^n=inf{cos(n*pi*x/L)*exp(-chi*n^2*pi^2*t/L^2)*...
#           (80/(3*(n*pi)^2))*cos(n*pi/2)*sin(n*pi/4)*sin(3*n*pi/20)}
# chi = K/(rho*Cp) 
#
# *****************************************************************************

import numpy as np
import math
import matplotlib.pyplot as plt
import sys

# Default options:
plot_flag = False
print_error = True
passing_crit = 2.  # [% error]

# Option parameters:
options = sys.argv[1:]
num_options = len(options)
for n in options:
  if n == 'print_error=false':
    print_error = False
  if n == 'print_error=true':
    print_error = True
  if n == 'plot_flag=false':
    plot_flag = False
  if n == 'plot_flag=true':
    plot_flag = True

# Create the analytical solution
K = 0.5787037  # [W/m-C]
Cp = 0.01      # [J/kg-C]
rho = 2000.    # [kg/m^3]
L = 100.0       # [m]
chi = K/(Cp*rho)
x_soln = np.linspace(0.5,99.5,100)          # [m]
t_soln = np.array([0.0,0.05,0.10,0.50])     # [day]
T_soln = np.zeros((4,100))
for time in range(4):
  t = t_soln[time]*24.0*3600.0  # [sec]
  sum_term = np.zeros(100)
  # truncate infinite sum to 500
  for n in range(500):
    n = n + 1
    sum_term = sum_term + (np.cos(n*math.pi*x_soln/L)*np.exp(-chi*pow(n,2)*pow(math.pi,2)*t/pow(L,2))*(80./(3.*pow((n*math.pi),2)))*np.cos(n*math.pi/2.)*np.sin(n*math.pi/4.)*np.sin(3.*n*math.pi/20.))
  T_soln[time,:] = 0.50 + sum_term
     
# Read PFLOTRAN output file containing the temperature solution
# There are four output files
T_pflotran = np.zeros((4,100))  # [C]

# 1:=========================================================================
f = open('1D_conduction_BC_1st_2nd_kind-000.vtk', 'r')
# Temperature solution is contained starting at the 617th line 
# and continues in chunks of 10 values, so we need to read all lines
# and concatenate them.
lines = f.readlines()
i = 616
# Get first line
lines[i] = lines[i].strip()
temperature = np.array(lines[i].split())
while i < 626:
  i = i + 1
  lines[i] = lines[i].strip()
  temperature = np.concatenate((temperature,np.array(lines[i].split())),axis=0)
temperature = temperature.astype(np.float)
T_pflotran[0,:] = temperature
# Close PFLOTRAN output file because we are done with it
f.close()

# 2:=========================================================================
f = open('1D_conduction_BC_1st_2nd_kind-001.vtk', 'r')
# Temperature solution is contained starting at the 617th line 
# and continues in chunks of 10 values, so we need to read all lines
# and concatenate them.
lines = f.readlines()
i = 616
# Get first line
lines[i] = lines[i].strip()
temperature = np.array(lines[i].split())
while i < 626:
  i = i + 1
  lines[i] = lines[i].strip()
  temperature = np.concatenate((temperature,np.array(lines[i].split())),axis=0)
temperature = temperature.astype(np.float)
T_pflotran[1,:] = temperature
# Close PFLOTRAN output file because we are done with it
f.close()

# 3:=========================================================================
f = open('1D_conduction_BC_1st_2nd_kind-002.vtk', 'r')
# Temperature solution is contained starting at the 617th line 
# and continues in chunks of 10 values, so we need to read all lines
# and concatenate them.
lines = f.readlines()
i = 616
# Get first line
lines[i] = lines[i].strip()
temperature = np.array(lines[i].split())
while i < 626:
  i = i + 1
  lines[i] = lines[i].strip()
  temperature = np.concatenate((temperature,np.array(lines[i].split())),axis=0)
temperature = temperature.astype(np.float)
T_pflotran[2,:] = temperature
# Close PFLOTRAN output file because we are done with it
f.close()

# 4:=========================================================================
f = open('1D_conduction_BC_1st_2nd_kind-003.vtk', 'r')
# Temperature solution is contained starting at the 617th line 
# and continues in chunks of 10 values, so we need to read all lines
# and concatenate them.
lines = f.readlines()
i = 616
# Get first line
lines[i] = lines[i].strip()
temperature = np.array(lines[i].split())
while i < 626:
  i = i + 1
  lines[i] = lines[i].strip()
  temperature = np.concatenate((temperature,np.array(lines[i].split())),axis=0)
temperature = temperature.astype(np.float)
T_pflotran[3,:] = temperature
# Close PFLOTRAN output file because we are done with it
f.close()

# Plot the PFLOTRAN and analytical solutions
if plot_flag:
  t_max = 1.5
  plt.subplot(221)
  plt.plot(x_soln,T_pflotran[0,:],'o',x_soln,T_soln[0,:])
  plt.xlabel('Distance (m)')
  plt.ylabel('Temperature (C)')
  plt.ylim([0,t_max])
  plt.xlim([0,100])
  plt.title('Analytical vs. PFLOTRAN Solution, t=0day')
  plt.legend(('PFLOTRAN','analytical'),'best',numpoints=1)
  plt.subplot(222)
  plt.plot(x_soln,T_pflotran[1,:],'o',x_soln,T_soln[1,:])
  plt.xlabel('Distance (m)')
  plt.ylabel('Temperature (C)')
  plt.ylim([0,t_max])
  plt.xlim([0,100])
  plt.title('Analytical vs. PFLOTRAN Solution, t=0.05day')
  plt.legend(('PFLOTRAN','analytical'),'best',numpoints=1)
  plt.subplot(223)
  plt.plot(x_soln,T_pflotran[2,:],'o',x_soln,T_soln[2,:])
  plt.xlabel('Distance (m)')
  plt.ylabel('Temperature (C)')
  plt.ylim([0,t_max])
  plt.xlim([0,100])
  plt.title('Analytical vs. PFLOTRAN Solution, t=0.10day')
  plt.legend(('PFLOTRAN','analytical'),'best',numpoints=1)
  plt.subplot(224)
  plt.plot(x_soln,T_pflotran[3,:],'o',x_soln,T_soln[3,:])
  plt.xlabel('Distance (m)')
  plt.ylabel('Temperature (C)')
  plt.ylim([0,t_max])
  plt.xlim([0,100])
  plt.title('Analytical vs. PFLOTRAN Solution, t=0.50day')
  plt.legend(('PFLOTRAN','analytical'),'best',numpoints=1)
  plt.show()

# Calculate error between analytical and PFLOTRAN solutions
# Shift both solutions to avoid dividing by zero
T_pflotran = T_pflotran + 0.5
T_soln = T_soln + 0.5
percent_error = 100.0*(T_pflotran-T_soln)/T_soln
max_percent_error = np.nanmax(abs(percent_error))
if print_error:
  print 'Percent Error (temperature):'
  print percent_error
print 'Maximum Error:'
print max_percent_error

# Decide if test passes
if abs(max_percent_error) > passing_crit:
  print '-- Test FAIL --\n'
else: 
  print '-- Test PASS --\n'
  



