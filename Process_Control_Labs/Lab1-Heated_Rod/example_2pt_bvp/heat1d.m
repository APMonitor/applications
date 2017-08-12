% 1-D heat conduction, unsteady state

function xdot=heat1d(t,x)

global u

n = size(x,1);

% Inputs (2):
% Left Surface Temperature (K)
Temp(1) = u(1);
% Right Surface Temperature (K)
Temp(n+2) = u(2);

% States (n):
% Internal nodes
Temp(2:n+1) = x(1:n,1)';

% Parameters:
% Thermal conductivity
k_silver = [436.13 -0.011922 -0.000084465 3.3463E-08 0];
k_alum = [165.84 0.49305 -0.0011114 9.8024E-07 -3.2368E-10];
A = k_alum;
for i = 1:n+2
	k(i) = A(1) + A(2)*Temp(i) + A(3)*Temp(i)^2 + A(4)*Temp(i)^3 + A(5)*Temp(i)^4;   
end
% use the harmonic mean to estimate the thermal conductivity at the control volume borders
for i = 1:n+1
   k_hm(i) = 2*k(i+1)*k(i) / (k(i)+k(i+1));
end

% Solid density
rho_silver = [102.79 -0.0186 0 0 0];
rho_alum = [102.83 -0.00873 0 0 0];
A = rho_alum;
for i = 1:n+2
	rho(i) = A(1) + A(2)*Temp(i) + A(3)*Temp(i)^2 + A(4)*Temp(i)^3 + A(5)*Temp(i)^4;   
end   

% Solid heat capacity
cp_silver = [24710 1.14 0.00388 0 0];
cp_alum = [22149 5.7062 0.0067408 0 0];
A = cp_alum;
for i = 1:n+2
	cp(i) = A(1) + A(2)*Temp(i) + A(3)*Temp(i)^2 + A(4)*Temp(i)^3 + A(5)*Temp(i)^4;   
end

% Width
width = 1;  % m
% Determine equal spacing between nodes
dx = width / (n+1);

%if (t>1)
%   dx
%end


% Compute xdot:
for i = 2:n+1,
   xdot(i-1,1) = (1/(rho(i)*cp(i)*dx)) * (k_hm(i)*(Temp(i+1)-Temp(i))/dx - k_hm(i-1)*(Temp(i)-Temp(i-1))/dx);
end

