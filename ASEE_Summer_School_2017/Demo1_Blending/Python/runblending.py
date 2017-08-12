# Run the blending process
# Martha Grover, July 6, 2017 (MATLAB)
# John Hedengren, July 14, 2017 (Python)

import numpy as np
from scipy.integrate import odeint

# Here is the playlist for the accompanying screencasts:
# https://www.youtube.com/playlist?list=PL4xAk5aclnUhb0tM6nypIATyxPRk0fB3L

# Following on the first screencast (Blending Process: Dynamic Simulation),
# here you can simulate the nonlinear coupled set of differential equations.
# As in the second screencast (Blending Process: Steady States), 
# observe here how the mass fraction in the tank 
# approaches the steady state value of xbar as the system approaches long 
# time.  The volume does not have a unique steady state.  Since filling a 
# tank is a integrating process, it may increase or decrease without bound, 
# based on the difference between the inlet and outlet mass flow rates.

# Parameters
rho = 1000   # Density [kg/m^3] 

# Here we will consider x1 and x2 to remain as constants
x1 = 0.1
x2 = 0

#######################################################################
############### Define the Nonlinear Model  ###########################
#######################################################################
# Nominal inputs: 
# x1: Mass fraction of Species A in Stream 1 (unitless)
# w1: Mass flow rate in Stream 1 [kg/s]
# x2: Mass fraction of Species A in Stream 2 (unitless)
# w2: Mass flow rate in Stream 2 [kg/s]
# w:  Outlet mass flow [kg/s]

def blending(z,t,u):
    # Dynamic model of the blending process
    # State variables passed in as vector z:
    V = z[0]   # Volume [m3]
    x = z[1]   # Mass fraction of Species A in the tank (unitless)
    # Inputs passed in as vector u:
    w1 = u[0]  # Mass flow rate in Stream 1 [kg/s]
    w2 = u[1]  # Mass flow rate in Stream 2 [kg/s]
    w = u[2]   # Here we set the outlet flow equal to the total inlet flow

    # Dynamic equations
    dVdt = (1.0/rho)*(w1+w2-w)                     # Change in volume
    dxdt = (1.0/(rho*V))*(w1*(x1-x)+w2*(x2-x))     # Change in mass fraction

    # Assemble the two time derivatives back into a vector to pass back
    dzdt = [dVdt,dxdt]
    return dzdt

#######################################################################
############# Dynamic Simulation of the Nonlinear System ##############
#######################################################################

# Initial conditions
V0 = 10        # Initial volume in the tank [m^3]
x0 = 0.025     # Initial mass fraction of Species A in the tank (unitless)
# Note: these are currently set at their nominal steady-state values...
# But you can try changing them to other values.
z0 = [V0,x0]  # Initial condition vector for the system

# The flow rates will be the variables in u that may change over time
w1 = 1         # w1: Mass flow rate in Stream 1 [kg/s]
w2 = 3         # w2: Mass flow rate in Stream 2 [kg/s]
w = w1 + w2    # w:  Outlet mass flow [kg/s]
u = [w1,w2,w]  # Assemble these together in a column vector u

tf = 3600      # Final simulation time [s]
t = np.linspace(0,tf,100) # points to report solution

# Simulate the blending process
z = odeint(blending,z0,t,args=(u,))

# plotting results
import matplotlib.pyplot as plt

# Plot the blending process under steady operation
plt.figure(1)
plt.subplot(2,1,1)
plt.plot(t,z[:,0])
plt.xlabel('time t [s]')
plt.ylabel('V [m^3]')
plt.title('Blending process under constant inputs')
plt.subplot(2,1,2)
plt.plot(t,z[:,1])
plt.xlabel('time t [s]')
plt.ylabel('x')

# Calculate the steady-state value for x 
xbar = (w1*x1 + w2*x2)/(w1+w2)
# Check to see if this matches the long-term value of x on the plot
# Since V does not have a unique steady state, specify a desired operating value
# Here it is set equal to the initial volume
Vbar = V0  # volume [m^3]

# Define ubar as the set of inputs to achieve this steady state
ubar = u

# Next simulate the system for the higher value of w1 = 1.1 (0.1 higher)
dw1 = 0.1
u[0] = ubar[0] + dw1

zs = odeint(blending,z0,t,args=(u,))

# Plot the blending process under a step change in w1
plt.figure(2)
plt.subplot(2,1,1)
plt.plot(t,zs[:,0])
plt.xlabel('time t [s]')
plt.ylabel('V [m^3]')
plt.title('Blending process under a step input to w_1')
plt.subplot(2,1,2)
plt.plot(t,zs[:,1])
plt.xlabel('time t [s]')
plt.ylabel('x')

# show plots
plt.show()


