clear all; close all; clc

% Numeric simulation
addpath('apm')
y = apm_solve('kettle');
z = y.x;

% Analytic solution
nsteps = 121;
time = linspace(0,120,nsteps);
for i = 1:nsteps,
    if (time(i)<=30),
        T(i) = (time(i)^2 * (4.28/30/2))/(3*4.18) + 18;
    else
        T(i) = (30^2 * (4.28/30/2) + 4.28 * (time(i)-30))/(3*4.18) + 18;
    end
end

figure(1)
plot(z.time,z.t,'r-','LineWidth',2)
hold on
plot(time,T,'b.-')
legend('Numeric','Analytic')
xlabel('Time (sec)')
ylabel('Temperature (degC)')
