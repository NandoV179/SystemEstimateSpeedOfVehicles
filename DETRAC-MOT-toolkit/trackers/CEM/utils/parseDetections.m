function [detections, nDets]=parseDetections(detectionSet, sceneInfo)
% read detection file and create a struct array
% 
% (C) Anton Andriyenko, 2012
%
% The code may be used free of charge for non-commercial and
% educational purposes, the only requirement is that this text is
% preserved within the derivative work. For any other purpose you
% must contact the authors for permission. This code may not be
% redistributed without written permission from the authors.

nDets=0;

%% now parse
cnt = numel(sceneInfo.frameNums);
detections(cnt).bx=[];
detections(cnt).by=[];
detections(cnt).xp=[];
detections(cnt).yp=[];
detections(cnt).ht=[];
detections(cnt).wd=[];
detections(cnt).sc=[];

detections(cnt).xi=[];
detections(cnt).yi=[];     
for t = 1:numel(sceneInfo.frameNums);
    idxObj = find(detectionSet(:, 1) == t);
    nObjects = numel(idxObj);
    bx =[];by=[];xp=[];yp=[];
    ht=[];wd=[];sc=[];
    xi=[];yi=[];           
    for j = 1:nObjects
        loc = detectionSet(idxObj(j), 3:6);
        score = detectionSet(idxObj(j), 7);         
        left = loc(1); top = loc(2);
        width = loc(3);
        height = loc(4);
        xis = left + width/2;
        yis = top + height;
        bx = cat(2, bx, left);
        by=cat(2, by, top);
        xp=cat(2, xp, xis);
        yp=cat(2, xp, yis);
        ht=cat(2, ht, height);
        wd=cat(2, wd, width);
        sc=cat(2, sc, score);
        xi=cat(2, xi, xis);
        yi=cat(2, yi, yis);     
    end
    detections(t).bx=bx;
    detections(t).by=by;
    detections(t).xp=xp;
    detections(t).yp=yp;
    detections(t).ht=ht;
    detections(t).wd=wd;
    detections(t).sc=sc;

    detections(t).xi=xi;
    detections(t).yi=yi; 

    nDets=nDets+length(xi);
end    

%% set xp and yp accordingly
detections = setDetectionPositions(detections);

end

function detections=setDetectionPositions(detections)
% set xp,yp to xi,yi if tracking is in image (2d)
% set xp,yp to xw,yi if tracking is in world (3d)
    F = length(detections);

    for t=1:F  
        detections(t).xp=detections(t).xi;
        detections(t).yp=detections(t).yi;
    end
end