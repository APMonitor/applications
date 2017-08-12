function dxdt = hab(t,x,parms)
%
% This function evaluates the ode rhs for the hot air balloon simulation.
%
% Tom Badgwell 06/07/17

% Get parameters

alpha = parms.alpha;
gamma = parms.gamma;
mu    = parms.mu;
omega = parms.omega;
delta = parms.delta;
beta  = parms.beta;

% Get inputs

u = parms.u;

% Calculate derivatives

dxdt = zeros(3,1);
Ths = 1 - delta*x(1);
dxdt(1) = x(2);
dxdt(2) = alpha*mu*(Ths^(gamma-1))*(1-(Ths/x(3))) - mu -omega*x(2)*abs(x(2));
dxdt(3) = -(x(3) - Ths)*(beta + u(2)) + u(1);

end
