function runblending()

% Run the blending process
% Martha Grover, July 6, 2017

% Here is the playlist for the accompanying screencasts:
% https://www.youtube.com/playlist?list=PL4xAk5aclnUhb0tM6nypIATyxPRk0fB3L

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%% Dynamic Simulation of the Nonlinear System %%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Following on the first screencast (Blending Process: Dynamic Simulation),
% here you can simulate the nonlinear coupled set of differential equations.
% As in the second screencast (Blending Process: Steady States), 
% observe here how the mass fraction in the tank 
% approaches the steady state value of xbar as the system approaches long 
% time.  The volume does not have a unique steady state.  Since filling a 
% tank is a integrating process, it may increase or decrease without bound, 
% based on the difference between the inlet and outlet mass flow rates.

clc
clear all
close all

% Parameters
global rho 
rho = 1000;   % Density [kg/m^3] 
tf = 3600;    % Final simulation time [s]

% Initial conditions
V0 = 10;        % Initial volume in the tank [m^3]
x0 = 0.025;     % Initial mass fraction of Species A in the tank (unitless)
% Note: these are currently set at their nominal steady-state values...
% But you can try changing them to other values.
z0 = [V0; x0];  % Initial condition vector for the system

% Nominal inputs: 
% x1: Mass fraction of Species A in Stream 1 (unitless)
% w1: Mass flow rate in Stream 1 [kg/s]
% x2: Mass fraction of Species A in Stream 2 (unitless)
% w2: Mass flow rate in Stream 2 [kg/s]
% w:  Outlet mass flow [kg/s]

% Here we will consider x1 and x2 to remain as constants
global x1 x2
x1 = 0.1;
x2 = 0;
% The flow rates will be the variables in u that may change over time
w1 = 1;         % w1: Mass flow rate in Stream 1 [kg/s]
w2 = 3;         % w2: Mass flow rate in Stream 2 [kg/s]
w = w1 + w2;    % w:  Outlet mass flow [kg/s]
u = [w1; w2; w];    % Assemble these together in a column vector u

% Simulate the blending process
[t,z] = ode45(@blending, [0 tf],z0,[],u);

% Plot the blending process under steady operation
figure(1)
subplot(2,1,1)
plot(t,z(:,1))
grid on
xlabel('time t [s]')
ylabel('V [m^3]')
title('Blending process under constant inputs')
subplot(2,1,2)
plot(t,z(:,2))
grid on
xlabel('time t [s]')
ylabel('x')

% Calculate the steady-state value for x 
xbar = (w1*x1 + w2*x2)/(w1+w2);
% Check to see if this matches the long-term value of x on the plot
% Since V does not have a unique steady state, specify a desired operating value
% Here it is set equal to the initial volume
Vbar = V0;  % volume [m^3]
% Define ubar as the set of inputs to achieve this steady state
ubar = u;

% Next simulate the system for the higher value of w1 = 1.1 (0.1 higher)
dw1 = 0.1;
u = ubar + [dw1; 0; 0];
[tstep,zstep] = ode45(@blending, [0 tf],z0,[],u);
% Plot the blending process under a step change in w1
figure(2)
subplot(2,1,1)
plot(tstep,zstep(:,1))
grid on
xlabel('time t [s]')
ylabel('V [m^3]')
title('Blending process under a step input to w_1')
subplot(2,1,2)
plot(tstep,zstep(:,2))
grid on
xlabel('time t [s]')
ylabel('x')

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%% Linear Approximate Model %%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Formulate the linear approximation as a state-space system using
% deviation variables (See screencast on Blending Process: Deviation
% Variables)

% Dynamic state x: V' and x'

% Inputs u: w1', w2', w'

% Measurements y: w1', V', x'

% Define the matrices A, B, C, and D for the linearized system
% dxdt = A*x + B*u' 
% y = C*x + D*u'
% See the screencasts on Linearization and State Space

% Dynamic equation: dx/dt = Ax + Bu
global A B
A = [0 0; 0 1/(rho*Vbar)*(-w1-w2)];   
B = [1/rho 1/rho -1/rho; 1/(rho*Vbar)*(x1-xbar) 1/(rho*Vbar)*(x2-xbar) 0];
% Measurement equation: y = Cx + Du
C = [0 0; 1 0; 0 1];            % Measuring the states V and x directly
D = [1 0 0; 0 0 0; 0 0 0];      % Measuring the input w directly

% Define input in deviation variables u'
up = u - ubar;
% Define the deviation in initial state
% Here we will continue to use z for the state vector, to avoid confusion 
% with the mass fraction of Species A which is called x
zbar = [Vbar; xbar];
zp0 = z0 - zbar;   % Note: We set z0 = zbar earlier, so this should be zero
% Simulate the linearized model of the blending process
[tp,zp] = ode45(@blending_linear,[0 tf],zp0,[],up);

% Plot the comparison between the nonlinear system and the linearized
% system, for a step change of 0.1 in w1
figure(3)
subplot(2,1,1)
plot(tstep,zstep(:,1),tp,zp(:,1)+Vbar)   
grid on
legend('Nonlinear','Linearized')
xlabel('time t [s]')
ylabel('volume V [m^3]')
title('Comparison of nonlinear and linear models for a step change in w_1')
subplot(2,1,2)
plot(tstep,zstep(:,2),tp,zp(:,2)+xbar)   
grid on
legend('Nonlinear','Linearized')
xlabel('time t [s]')
ylabel('mass fraction x')

% In this example, the linear model agrees pretty well with the nonlinear 
% model.  The equation for volume V is linear and does not depend on the 
% mass fraction x, so it agrees perfectly with the nonlinear model.
% The mass fraction prediction is not perfect, but because the step change
% is "small" (10%) the agreement is still pretty good.

% Steady-state gain of the system
K = C*pinv(-A)*B+D;
% Note: It is not possible to calculate this since A is not invertible
% This makes sense because there is no unique steady-state value for
% volume V

% Note that we did not actually use C and D in this example.  We can
% evaluate the measurements y' at each time point of our ode solution:
yp = zeros(length(ubar),length(tp));
for i = 1:length(tp)
   yp(:,i) = C*zp(i,:)' + D*up;
end

end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%% Define the Nonlinear and Linear Models %%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function dzdt = blending(t,z,u)
% Dynamic model of the blending process
% Martha Grover, July 6, 2017
% State variables passed in as vector z:
V = z(1);   % Volume [m3]
x = z(2);   % Mass fraction of Species A in the tank (unitless)
% Mass fractions in Streams 1 and 2: x1 and x2
global x1 x2
% Inputs passed in as vector u:
w1 = u(1);  % Mass flow rate in Stream 1 [kg/s]
w2 = u(2);  % Mass flow rate in Stream 2 [kg/s]
w = u(3);   % Here we set the outlet flow equal to the total inlet flow

% Density rho
global rho

% Dynamic equations
dVdt = 1/rho*(w1+w2-w);                     % Change in volume
dxdt = 1/(rho*V)*(w1*(x1-x)+w2*(x2-x));     % Change in mass fraction

% Assemble the two time derivatives back into a vector to pass back
dzdt = [dVdt; dxdt];

end

function dxdt = blending_linear(t,x,u)
% State space version of the linearized model for the blending process,
% using deviation variables
% dx/dt = A*x + B*u
% The measurement equation of y = C*x + D*u is not included here, since
% it is an algebraic equation that does not need to be solved by ode45.
% Martha Grover, July 6, 2017

% Dynamic state x
Vp = x(1);      % V' = deviation in volume
xp = x(2);      % x' = deviation in mass fraction

% Input vector u 
w1p = u(1);     % w1' = deviation in mass flow rate in inlet Stream 1
w2p = u(2);     % w2' = deviation in mass flow rate in inlet Stream 2
wp = u(3);      % w' = deviation in mass fraction in outlet stream

% Use the values in A and B defined in the main script
global A B

% dx/dt = Ax + Bu
dxdt = A*x + B*u;

end






