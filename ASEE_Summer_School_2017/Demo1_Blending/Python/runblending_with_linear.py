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
plt.ylabel(r'$V \; [m^3]$')
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
ubar = np.copy(u)

# Next simulate the system for the higher value of w1 = 1.1 (0.1 higher)
dw1 = 0.1
u[0] = ubar[0] + dw1

zs = odeint(blending,z0,t,args=(u,))

# Plot the blending process under a step change in w1
plt.figure(2)
plt.subplot(2,1,1)
plt.plot(t,zs[:,0])
plt.xlabel('time t [s]')
plt.ylabel(r'$V \; [m^3]$')
plt.title(r'Blending process under a step input to $w_1$')
plt.subplot(2,1,2)
plt.plot(t,zs[:,1])
plt.xlabel('time t [s]')
plt.ylabel('x')


#######################################################################
###################### Linear Approximate Model #######################
#######################################################################

# Formulate the linear approximation as a state-space system using
# deviation variables (See screencast on Blending Process: Deviation
# Variables)

# Dynamic state x: V' and x'

# Inputs u: w1', w2', w'

# Measurements y: w1', V', x'

# Define the matrices A, B, C, and D for the linearized system
# dxdt = A*x + B*u' 
# y = C*x + D*u'
# See the screencasts on Linearization and State Space

# Dynamic equation: dx/dt = Ax + Bu
A = np.array([[0,0], \
              [0,1.0/(rho*Vbar)*(-w1-w2)]])   
B = np.array([[1.0/rho,1.0/rho,-1.0/rho], \
              [1.0/(rho*Vbar)*(x1-xbar),1.0/(rho*Vbar)*(x2-xbar),0]])
# Measurement equation: y = Cx + Du
C = np.array([[0,0], \
              [1,0], \
              [0,1]])        # Measuring the states V and x directly
D = np.array([[1,0,0], \
              [0,0,0], \
              [0,0,0]])      # Measuring the input w directly

              
#######################################################################
############### Define the Linear Model ###############################
#######################################################################
def blending_linear(x,t,u):
    # State space version of the linearized model for the blending process,
    # using deviation variables
    # dx/dt = A*x + B*u
    # The measurement equation of y = C*x + D*u is not included here, since
    # it is an algebraic equation that does not need to be solved by odeint.

    # Dynamic state x
    Vp = x[0]      # V' = deviation in volume
    xp = x[1]      # x' = deviation in mass fraction

    # Input vector u 
    w1p = u[0]     # w1' = deviation in mass flow rate in inlet Stream 1
    w2p = u[1]     # w2' = deviation in mass flow rate in inlet Stream 2
    wp = u[2]      # w' = deviation in mass fraction in outlet stream

    # dx/dt = Ax + Bu
    dxdt = np.dot(A,x) + np.dot(B,u)
    return dxdt
              
# Define input in deviation variables u'
up = np.array(u) - np.array(ubar)
# Define the deviation in initial state
# Here we will continue to use z for the state vector, to avoid confusion 
# with the mass fraction of Species A which is called x
zbar = np.array([Vbar,xbar])
zp0 = z0 - zbar   # Note: We set z0 = zbar earlier, so this should be zero
# Simulate the linearized model of the blending process
zp = odeint(blending_linear,zp0,t,args=(up,))

# Plot the comparison between the nonlinear system and the linearized
# system, for a step change of 0.1 in w1
plt.figure(3)
plt.subplot(2,1,1)
plt.plot(t,zs[:,0],'r-',linewidth=2)
plt.plot(t,zp[:,0]+Vbar,'b--',linewidth=2)
plt.legend(['Nonlinear','Linearized'])
plt.xlabel('time t [s]')
plt.ylabel(r'$V \; [m^3]$')
plt.title(r'Comparison of nonlinear and linear models for a step change in $w_1$')
plt.subplot(2,1,2)
plt.plot(t,zs[:,1],'k-',linewidth=2)
plt.plot(t,zp[:,1]+xbar,'g:',linewidth=2)
plt.legend(['Nonlinear','Linearized'])
plt.xlabel('time t [s]')
plt.ylabel('mass fraction x')

# In this example, the linear model agrees pretty well with the nonlinear 
# model.  The equation for volume V is linear and does not depend on the 
# mass fraction x, so it agrees perfectly with the nonlinear model.
# The mass fraction prediction is not perfect, but because the step change
# is "small" (10%) the agreement is still pretty good.

# Steady-state gain of the system
K = np.dot(np.dot(C,np.linalg.pinv(-A)),B)+D

# Note: It is not possible to calculate this since A is not invertible
# This makes sense because there is no unique steady-state value for
# volume V

# Note that we did not actually use C and D in this example.  We can
# evaluate the measurements y' at each time point of our ode solution:
yp = np.zeros((np.size(ubar),np.size(t)))
yp = np.dot(C,zp.T)
for i in range(np.size(t)):
    yp[:,i] = yp[:,i] + np.dot(D,up)

# show plots
plt.show()


