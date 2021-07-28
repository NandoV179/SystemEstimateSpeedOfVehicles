function [stateInfo, speed] = run_tracker(curSequence, baselinedetections)
%% Multi-Target Tracking by Continuous Energy Minimization

%% declare global variables
global cemStartTime detMatrices detections sceneInfo opt globiter 
globiter=0;

%% setup options and scene
% fill options struct
opt = getConOptionsDemo();
opt.print = 0;
opt.display = 0;
% energy weights (default 2d)

opt.weightEdet=1;               % should be kept at 1
opt.weightEdyn=0.03;
opt.weightEexc=0.5;
opt.weightEper=0.3;
opt.weightEreg=0.1;
opt.weightEapp=0.;

 
% fill scene info
sceneInfo = getSceneInfoConDemo(curSequence);
%% load detections
detections = parseDetections(baselinedetections, sceneInfo); 
stateInfo.F = size(detections,2);
detMatrices = getDetectionMatrices(detections);
cemStartTime = tic;
%% init solution
X=[]; Y=[];
initsolfile = fullfile('demo','ekf','e0001.mat');
load(initsolfile);
[X, Y] = checkInitSolution(X,Y,stateInfo.F);

stateInfo.N = size(X,2);
stateInfo.targetsExist = getTracksLifeSpans(X);
stateInfo.frameNums = sceneInfo.frameNums;
stateInfo = matricesToVector(X,Y,stateInfo);
[~, ~, F, ~, stateInfo.X, stateInfo.Y] = getStateInfo(stateInfo);

%% initial gradient descent (if initial solution available)
if(~isempty(stateInfo.stateVec))
    [stateInfo.stateVec, Evalue, nIterations] = minimize(stateInfo.stateVec,'E',opt.maxIterCGD,stateInfo);
end

%% now do main optimization
converged = false;
epoch = 0;
while(~converged && epoch<opt.maxEpochs)
    epoch = epoch+1;
%                     printMessage(1,'---- JUMP  MOVES  ROUND %i ----\n',epoch);
    jumpExecuted = false(1,6);

    for jumpMove = opt.jumpsOrder
        stateInfoOld = stateInfo;
        eval(sprintf('stateInfo=%s(stateInfo);',getJumpMoveFunction(jumpMove)))

        % did we jump?
        if isequal(stateInfoOld,stateInfo) % no
            printMoveFailure(jumpMove);       
        %  perform conjugate gradient descent if move was successful
        else  
            jumpExecuted(jumpMove)=1;
            [stateInfo.stateVec, Evalue, nIterations] = minimize(stateInfo.stateVec,'E',opt.maxIterCGD,stateInfo);
        end
    end

    % if no jumps were perfomed, we're done
    if all(~jumpExecuted)
        converged=true;
%         printMessage(1,'No jumps were executed. Optimization has converged after %i epochs.\n',epoch);
    end

    % if last epoch
    if(epoch >= opt.maxEpochs)
%         printMessage(1,'Max number of rounds reached.\n');
    end
end % converged

% basically we are done
speed = F/toc(cemStartTime);
%% post processing
% get X Y matrices
[stateVec, N, F, targetsExist, stateInfo.X, stateInfo.Y] = getStateInfo(stateInfo);
stateInfo = postProcessState(stateInfo);