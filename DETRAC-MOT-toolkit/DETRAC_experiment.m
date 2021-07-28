% This script can be used to execute the tracking experiments or evaluate the detection results on the UA-DETRAC benchmark
% Copyright (C)2016 The UA-DETRAC Group 

% This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by
% the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

% This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
% MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

% You should have received a copy of the GNU General Public License along with this program. If not, see <http://www.gnu.org/licenses/>.

clear, clc, close all;
warning off all;
global options sequences tracker

%% add the path of functions
addpath(genpath('D:\UA-DETRAC\DETRAC-MOT-toolkit\utils'));
addpath(genpath('D:\UA-DETRAC\DETRAC-MOT-toolkit\evaluation'));
addpath(genpath('D:\UA-DETRAC\DETRAC-MOT-toolkit\evaluation\display'));

%% input the name of the tracker
tracker.trackerName = 'GOG'; % ignore this line when evaluating detection results
%% initialize the parameters for evalution
options = initialize_environment();
%% load the dataset
sequences = load_datasets();
%% evaluate the tracker
run_experiment();