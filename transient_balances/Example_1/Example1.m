clear all; close all; clc

% Numeric simulation
addpath('apm')
y = apm_solve('tank');
z = y.x;

% Analytic solution
time = z.time;
h = (2 - 1.2 * exp(-0.4*time/pi()))/0.4;

figure(1)
plot(time,z.h,'r-','LineWidth',2)
hold on
plot(time,h,'b.-')
legend('Numeric','Analytic')
xlabel('Time (sec)')
ylabel('Height (m)')
