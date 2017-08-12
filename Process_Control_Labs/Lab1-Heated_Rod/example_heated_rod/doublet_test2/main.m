% clear everything
clc; clear all; close all

% load apm libraries
addpath('apm')

% generate results
z = apm_solve('rod');

% save data for FOPDT model fit
y = z.x;
data = [y.time(4:end) y.t_heater(4:end) y.t100(4:end)];
save -ascii data.txt data

% plot results
figure(1)
subplot(3,1,1)
plot(y.time,y.t_heater)
ylabel('T_{heater} (K)')
legend('T_{heater}')
subplot(3,1,2)
plot(y.time,y.t1,'r-')
hold on
plot(y.time,y.t5,'b-')
plot(y.time,y.t15,'k-')
plot(y.time,y.t25,'g-')
plot(y.time,y.t35,'m-')
plot(y.time,y.t45,'r.-')
plot(y.time,y.t55,'b.-')
plot(y.time,y.t65,'k.-')
plot(y.time,y.t75,'g.-')
plot(y.time,y.t85,'m.-')
plot(y.time,y.t95,'r--')
plot(y.time,y.t100,'b--')
ylabel('T_i (K)')
subplot(3,1,3)
plot(y.time,y.t100,'b-')
ylabel('T_{tip} (K)')
legend('T_{tip}')
xlabel('time (sec)')
