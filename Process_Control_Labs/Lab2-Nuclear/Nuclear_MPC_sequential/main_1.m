clc; clear all; close all
% make APM libraries available
addpath('apm');
        
% Select server
% server = 'http://xps.apmonitor.com';
server = 'http://localhost';
%server = 'http://byu.apmonitor.com';
% Application name
app = 'mpc';

% Clear previous application
apm(server,app,'clear all');

% Load model file
apm_load(server,app,'mpc.apm');

% Load time points for future predictions
csv_load(server,app,'time.csv');% for time  
load demand_data.txt
demand_data=demand_data; % data to replay for the controller

% APM Variable Classification
% class = FV, MV, SV, CV
%   F or FV = Fixed value - parameter may change to a new value every cycle
%   M or MV = Manipulated variable - independent variable over time horizon
%   S or SV = State variable - model variable for viewing
%   C or CV = Controlled variable - model variable for control

%Parameters
apm_info(server,app,'FV','demand'); %
apm_info(server,app,'MV','SPnuc'); %
apm_info(server,app,'MV','SPlng'); %
apm_info(server,app,'MV','SPbat'); %
%Variables
apm_info(server,app,'CV','nuc'); % 
apm_info(server,app,'CV','lng');
apm_info(server,app,'CV','bat');
apm_info(server,app,'CV','prod');% production

% controller mode (1=simulate, 2=predict, 3=control)
apm_option(server,app,'nlc.reqctrlmode',3); % 

% time units (1=sec,2=min,3=hrs,etc)
apm_option(server,app,'nlc.ctrl_units',3);
apm_option(server,app,'nlc.hist_units',3);
% set controlled variable error model type
apm_option(server,app,'nlc.cv_type',1);
% apm_option(server,app,'nlc.ev_type',1);% estimated variable type

% read discretization from CSV file
apm_option(server,app,'nlc.csv_read',1);

% turn on historization to see past results
apm_option(server,app,'nlc.hist_hor',500);

% set web plot update frequency
apm_option(server,app,'nlc.web_plot_freq',1);

% Objective for Nonlinear Control

% Controlled variable (c)
apm_option(server,app,'nuc.sphi',80);   % Upper set point; Set point high for linear error model
apm_option(server,app,'nuc.splo',20);   % Lower set point; Set point low for linear error model
apm_option(server,app,'nuc.wsphi',300);   %Objective function weight on upper set point for linear error model
apm_option(server,app,'nuc.wsplo',50);   % Objective function weight on lower set point for linear error model
apm_option(server,app,'nuc.cost',0.01);   % Lower set point weight, (+)=minimize, (-)=maximize
apm_option(server,app,'nuc.tr_init',2);  % Traj initialization (0=dead-band, 1=re-center with coldstart/out-of-service, 2=re-center always)
apm_option(server,app,'nuc.tr_open',0.1); %Initial trajectory opening ratio (0=ref traj, 1=tunnel, 2=funnel)
apm_option(server,app,'nuc.tau',80);    % Time constant for controlled variable response (time to reach ~60% of the new sp), only used when tr_int is 1 or 2
apm_option(server,app,'nuc.status',0);   % 1 = ON, 0 = OFF
apm_option(server,app,'nuc.fstatus',0);  % feedback status, 0=off

apm_option(server,app,'lng.sphi',15);   % Upper set point; Set point high for linear error model
apm_option(server,app,'lng.splo',0);   % Lower set point; Set point low for linear error model
apm_option(server,app,'lng.wsphi',300);   %Objective function weight on upper set point for linear error model
apm_option(server,app,'lng.wsplo',50);   % Objective function weight on lower set point for linear error model
apm_option(server,app,'lng.cost',0.1);   % Lower set point weight, (+)=minimize, (-)=maximize
apm_option(server,app,'lng.tr_init',2);  % Traj initialization (0=dead-band, 1=re-center with coldstart/out-of-service, 2=re-center always)
apm_option(server,app,'lng.tr_open',0.1); %Initial trajectory opening ratio (0=ref traj, 1=tunnel, 2=funnel)
apm_option(server,app,'lng.tau',5);    % Time constant for controlled variable response (time to reach ~60% of the new sp), only used when tr_int is 1 or 2
apm_option(server,app,'lng.status',0);   % 1 = ON, 0 = OFF
apm_option(server,app,'lng.fstatus',0);  % feedback status, 0=off

apm_option(server,app,'bat.sphi',2);   % Upper set point; Set point high for linear error model
apm_option(server,app,'bat.splo',0);   % Lower set point; Set point low for linear error model
apm_option(server,app,'bat.wsphi',300);   %Objective function weight on upper set point for linear error model
apm_option(server,app,'bat.wsplo',50);   % Objective function weight on lower set point for linear error model
apm_option(server,app,'bat.cost',1);   % Lower set point weight, (+)=minimize, (-)=maximize
apm_option(server,app,'bat.tr_init',2);  % Traj initialization (0=dead-band, 1=re-center with coldstart/out-of-service, 2=re-center always)
apm_option(server,app,'bat.tr_open',0.1); %Initial trajectory opening ratio (0=ref traj, 1=tunnel, 2=funnel)
apm_option(server,app,'bat.tau',0.5);    % Time constant for controlled variable response (time to reach ~60% of the new sp), only used when tr_int is 1 or 2
apm_option(server,app,'bat.status',0);   % 1 = ON, 0 = OFF
apm_option(server,app,'bat.fstatus',0);  % feedback status, 0=off

apm_option(server,app,'prod.sphi',80);   % Upper set point; Set point high for linear error model
apm_option(server,app,'prod.splo',20);   % Lower set point; Set point low for linear error model
apm_option(server,app,'prod.wsphi',50);   %Objective function weight on upper set point for linear error model
apm_option(server,app,'prod.wsplo',500);   % Objective function weight on lower set point for linear error model
apm_option(server,app,'prod.cost',1);   % Lower set point weight, (+)=minimize, (-)=maximize
apm_option(server,app,'prod.tr_init',0);  % Traj initialization (0=dead-band, 1=re-center with coldstart/out-of-service, 2=re-center always)
apm_option(server,app,'prod.tr_open',0.1); %Initial trajectory opening ratio (0=ref traj, 1=tunnel, 2=funnel)
apm_option(server,app,'prod.tau',80);    % Time constant for controlled variable response (time to reach ~60% of the new sp), only used when tr_int is 1 or 2
apm_option(server,app,'prod.status',1);   % 1 = ON, 0 = OFF
apm_option(server,app,'prod.fstatus',0);  % feedback status, 0=off



% Manipulated variables (u)
apm_option(server,app,'SPnuc.upper',100);
apm_option(server,app,'SPnuc.dmax',15);% Delta MV maximum step per horizon interval
apm_option(server,app,'SPnuc.lower',20);
apm_option(server,app,'SPnuc.status',1);
apm_option(server,app,'SPnuc.fstatus',0);

apm_option(server,app,'SPlng.upper',10);
apm_option(server,app,'SPlng.dmax',10);% Delta MV maximum step per horizon interval
apm_option(server,app,'SPlng.lower',0);
apm_option(server,app,'SPlng.status',1);
apm_option(server,app,'SPlng.fstatus',0);

apm_option(server,app,'SPbat.upper',1);
apm_option(server,app,'SPbat.dmax',1);% Delta MV maximum step per horizon interval
apm_option(server,app,'SPbat.lower',0);
apm_option(server,app,'SPbat.status',1);
apm_option(server,app,'SPbat.fstatus',0);


% imode (1=ss, 2=mpu, 3=rto, 4=sim, 5=mhe, 6=nlc)
%apm_option(server,app,'nlc.imode',3);
%solver_output = apm(server,app,'solve');

% apm_var(server,app);
% disp('Opening web viewer');
% apm_web(server,app);
% break
apm_option(server,app,'nlc.imode',6);

for isim = 1:size(demand_data,1) % 

   % update time step
   
    
   % update demand 
   demand = demand_data(isim,2);
   apm_meas(server,app,'demand',demand); % 
   apm_option(server,app,'prod.sphi',demand+0.5);   % Upper set point; Set point high for linear error model
   apm_option(server,app,'prod.splo',demand);   % Lower set point; Set point low for linear error model

   % Run NLC on APM server
   solver_output = apm(server,app,'solve');
   disp(solver_output)

   if (isim==1),
      % Open Web Viewer and Display Link
      disp('Opening web viewer');
      url = apm_web(server,app);
   end
end