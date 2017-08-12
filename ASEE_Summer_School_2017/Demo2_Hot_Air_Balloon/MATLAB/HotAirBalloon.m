% This script simulates a Hot Air Balloon, type AX7-77 from Head Balloons, 
% Inc.
%
% Tom Badgwell 06/07/17

% Set hot air balloon parameters

parms.alpha = 5.098;
parms.gamma = 5.257;
parms.mu    = 0.1961;
parms.omega = 8.544;
parms.delta = 0.0255;
parms.beta  = 0.01683;

% Set the variable scaling parameters

hr = 1000;  % meters
tr = 10.10; % seconds
Tr = 288.2; % K
fr = 4870;  % %
pr = 1485;  % %

% Initialize simulation variables

t0       = 0;
tf       = 5000;
dt       = 0.25;
N        = round((tf-t0)/dt) + 1;
% xstart   = [0.0; 0.0; 1.244]; % neutral buoyancy
xstart   = [0.0; 0.0; 1.000]; % ambient temperature
tstart   = 0;
fk       = zeros(N,1);
pk       = zeros(N,1);
uk       = zeros(N,2);
xk       = zeros(N,3);
yk       = zeros(N,3);
tm       = zeros(N,1);
xk(1,:)  = xstart;
C        = eye(3);
yk(1,:)  = C*xstart;
tm(1)    = 0;

% Initial conditions

fk(   1:1000) =  0.0;
pk(   1:1000) =  0.0;

% Warm up to nuetral buoyancy

fk(1001:3000) = 20.0;
pk(1001:3000) =  0.0;

% Takeoff

fk(3001:5000) = 25.0;
pk(3001:5000) =  0.0;

% Climb higher

fk(5001:7000) = 30.0;
pk(5001:7000) =  0.0;

% Open the vent

fk(7001:9000) = 30.0;
pk(7001:9000) =  5.0;

% Close the vent

fk(9001:11000) = 30.0;
pk(9001:11000) =  0.0;

% Descend

fk(11001:13000) = 22.0;
pk(11001:13000) =  0.0;

% Descend

fk(13001:15000) = 21.0;
pk(13001:15000) =  0.0;

% Land

fk(15001:17000) = 20.0;
pk(15001:17000) =  0.0;

% Close fuel valve and open the vent valve

fk(17001:N) =   0.0;
pk(17001:N) =   5.0;

% Make inputs dimensionless

uk(:,1) = (fk/fr);
uk(:,2) = (pk/pr);

% Run the simulation

for k = 2:N
    
    % Output iteration count
    
    %fprintf('iteration %i \n',k )
    
    % Integrate the model for this time step
    
    parms.u = uk(k,:);
    tstop   = tstart + dt;
    tspan   = [tstart tstop];
    [t,x]   = ode45(@(t,x) hab(t,x,parms), tspan, xstart);
    
    % Impose constraints when on the ground
    
    if (x(end,1) <= 0.0)
        x(end,1) = 0.0;
        x(end,2) = 0.0;
    end
        
    % Store solution
                
    xk(k,:) = x(end,:);
    yk(k,:) = C*xk(k,:)';
    tm(k)   = tr*tstop;
        
    % Set initial state
    
    xstart = xk(k,:);
    tstart = tstop;
    
end

% Recover dimensional outputs

hk  = yk(:,1)*hr;
vk  = yk(:,2)*hr/tr;
Tik = yk(:,3)*Tr - 273.2;

% Convert time to minutes

tmm = tm/60;

% Plot results

figure(1);

subplot(5,1,1);
plot(tmm,hk)
axis([1 tmm(N) -100 4000]);
grid;
ylabel('altitude (m)');
xlabel('time (minutes)');

subplot(5,1,2);
plot(tmm,vk)
axis([1 tmm(N) -4 4 ]);
grid;
ylabel('velocity (m/s)');
xlabel('time (minutes)');

subplot(5,1,3);
plot(tmm,Tik)
axis([1 tmm(N) 14 100]);
grid;
ylabel('temperature (C)');
xlabel('time (minutes)');

subplot(5,1,4);
plot(tmm,fk)
axis([1 tmm(N) -1 31]);
grid;
ylabel('fuel valve (%)');
xlabel('time (minutes)');

subplot(5,1,5);
plot(tmm,pk)
axis([1 tmm(N) -1 6]);
grid;
ylabel('vent valve (%)');
xlabel('time (minutes)');



