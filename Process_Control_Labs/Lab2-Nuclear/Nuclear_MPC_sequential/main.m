% Clear local variables and plots
clc; clear all; close all

% Add APM libraries to path for session
addpath('apm');

% Integrate model and return solution
z = apm_optimize('mpc')

figure(1)
plot(z.time,z.demand,'k-','LineWidth',3)
hold
plot(z.time,z.prod,'r.')
plot(z.time,z.nuc,'b--')
plot(z.time,z.lng,'r--')
plot(z.time,z.bat,'g--')
plot(z.time,z.spnuc,'b.-')
plot(z.time,z.splng,'r.-')
plot(z.time,z.spbat,'g.-')
xlabel('Time (hours)')
ylabel('Power (MW_e)')
legend('Demand','Production','Nuclear','LNG','Battery',...
    'SP_{Nuclear}','SP_{LNG}','SP_{Battery}')