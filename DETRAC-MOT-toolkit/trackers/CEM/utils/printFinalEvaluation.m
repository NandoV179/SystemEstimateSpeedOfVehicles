function printFinalEvaluation(stateInfo)
% 
% (C) Anton Andriyenko, 2012
%
% The code may be used free of charge for non-commercial and
% educational purposes, the only requirement is that this text is
% preserved within the derivative work. For any other purpose you
% must contact the authors for permission. This code may not be
% redistributed without written permission from the authors.

global sceneInfo gtInfo opt

if(sceneInfo.gtAvailable && opt.print)
    printMessage(1,'\nEvaluation 2D:\n');
    [metrics, metricsInfo] = CLEAR_MOT(gtInfo,stateInfo);
    printMetrics(metrics,metricsInfo,1);
end