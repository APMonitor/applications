clear all; close all; clc

% Numeric simulation
addpath('apm')
y = apm_solve('funnel');
z = y.x;

% Analytic solution
time = z.time;
a = 0.05*sqrt(1000*9.81/0.9);
h = (-5*a/pi()/2 * time + 10^(5/2)).^(2/5);

figure(1)
plot(time,z.h,'r-','LineWidth',2)
hold on
plot(time,h,'b.-')
legend('Numeric','Analytic')
xlabel('Time (sec)')
ylabel('Height (cm)')
