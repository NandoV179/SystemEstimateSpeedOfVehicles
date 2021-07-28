function opt=getConOptionsDemo(w)
% 
% (C) Anton Andriyenko, 2012
%
% The code may be used free of charge for non-commercial and
% educational purposes, the only requirement is that this text is
% preserved within the derivative work. For any other purpose you
% must contact the authors for permission. This code may not be
% redistributed without written permission from the authors.

% general
opt.track3d=0;                  % set to 1 for track estimation on ground plane
opt.verbosity=1;                % 0=silent, 1=short info, 2=long info, 3=all
opt.mex=1;                      % use mex
opt.visOptim=0;                 % visualize optimization
opt.occ=0;                      % compute occlusions [Andriyenko et al. ICCV VS Workshop 2011]
                                % only works for 3d tracking for now!
opt.cutToTA=0;                  % cut detections, ground truth and result to tracking area

% optimization
opt.jumpsOrder = [1 3 4 2 6 5];   % standard: merge grow shrink split add remove
opt.maxEpochs = 15;                % max global iterations (rounds)
opt.maxIterCGD = 30;              % max iterations for each gradient descent

% energy weights (default 2d)
opt.weightEdet=1;               % should be kept at 1
opt.weightEdyn=0.0;
opt.weightEexc=0.52;
opt.weightEper=0.5;
opt.weightEreg=0.6;
opt.weightEapp=0.;

% other parameters
opt.lambda=0.125;

if nargin==1
    opt.weightEdet=w(1);               % should be kept at 1
    opt.weightEdyn=w(2);
    opt.weightEexc=w(3);
    opt.weightEper=w(4);
    opt.weightEreg=w(5);
    opt.weightEreg=w(6);    
end

end