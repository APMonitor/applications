clear all
close all

global u

% Number of internal nodes
n = 20;

% Steady State Initial Conditions for the borders
u(1) = 25 + 273.15;
u(2) = 25 + 273.15;

% Steady State Initial Conditions for the States
for i = 2:n+1,
   T(i) = 25 + 273.15;
end

% Change temperature on the left side
u(1) = 100 + 273.15;


% Initial conditions
x0(1:n,1) = T(2:n+1)';

% Final Time (sec)
tf = 600;
%tspan = [0 5 10 20 50 300];
tspan = linspace(0,tf,10);

[t,x] = ode15s('heat1d',tspan,x0);

[m,n] = size(x);

% Parse out the state values
T(1) = u(1);
T(2:n+1) = x(m,:);
T(n+2) = u(2);

% Width
width = 1;  % m
% Determine equal spacing between nodes
dx = width / (n+1);

dist(1) = 0;
for i = 2:n+2,
   dist(i) = dist(i-1) + dx;
end

% Plot the results
figure(1);
plot(dist,T);
xlabel('Distance (m)')
ylabel('Temperature (K)')
hold on;