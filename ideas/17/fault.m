clc;
clear all;

% Open the Simulink model
open('IEEE_9bus_new_o.slx');

% Simulate the Simulink model
sim('IEEE_9bus_new_o.slx');

% Assign the outputs of the simulation
currentA = current1; % Phase A current
currentB = current2; % Phase B current
currentC = current3; % Phase C current
currentG = current4; % Ground current

% Perform wavelet decomposition - 'db4' wavelet at level 1
[cA, LA] = wavedec(currentA, 1, 'db4'); % Phase A decomposition
[cB, LB] = wavedec(currentB, 1, 'db4'); % Phase B decomposition
[cC, LC] = wavedec(currentC, 1, 'db4'); % Phase C decomposition
[cG, LG] = wavedec(currentG, 1, 'db4'); % Ground decomposition

% Extract detailed coefficients at level 1
coefA = detcoef(cA, LA, 1); % Phase A coefficients
coefB = detcoef(cB, LB, 1); % Phase B coefficients
coefC = detcoef(cC, LC, 1); % Phase C coefficients
coefG = detcoef(cG, LG, 1); % Ground coefficients

% Find the maximum detailed coefficient values for analysis
m = max(coefA); % Max coefficient for Phase A
n = max(coefB); % Max coefficient for Phase B
p = max(coefC); % Max coefficient for Phase C
q = max(coefG); % Max coefficient for Ground
