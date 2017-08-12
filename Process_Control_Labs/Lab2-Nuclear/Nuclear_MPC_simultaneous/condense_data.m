clc; clear all; close all

% load data file
load data.txt

% reduce data down to about 500 data points over 24 hours
m = int16(size(data,1)/500);
new = data(1,:);
for i = 1:size(data,1),
    if (mod(i,m)==0),
        new = [new; data(i,:)];
    end
end
new = [new; data(end,:)];

save -ascii condensed_data.txt new
