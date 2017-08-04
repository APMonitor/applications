clear all; close all; clc

% Numeric simulation
addpath('apm')
y = apm_solve('tank2');
z = y.x;

% Analytic solution
time = z.time;
xsalt = 4 * exp(-time*5/100);

figure(1)
plot(time,z.xsalt,'r-','LineWidth',2)
hold on
plot(time,xsalt,'b.-')
legend('Numeric','Analytic')
xlabel('Time (sec)')
ylabel('Concentration (lb_m salt/gal)')
