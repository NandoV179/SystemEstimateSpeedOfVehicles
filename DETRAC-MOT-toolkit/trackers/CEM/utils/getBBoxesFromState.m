function stateInfo=getBBoxesFromState(stateInfo)
% for visualization and for 2D evaluation
% we need the bounding boxes of the targets
% To this end, we check for corresponding detections
% and interpolate them to get the solution boxes
% 
% (C) Anton Andriyenko, 2012
%
% The code may be used free of charge for non-commercial and
% educational purposes, the only requirement is that this text is
% preserved within the derivative work. For any other purpose you
% must contact the authors for permission. This code may not be
% redistributed without written permission from the authors.

global detections sceneInfo
X=stateInfo.X; Y=stateInfo.Y;

[F, N]=size(X);
targetsExist=getTracksLifeSpans(X);

W=zeros(size(X));
H=zeros(size(Y));


for id=1:N
    sid=targetsExist(id,1);
    eid=targetsExist(id,2);
    frames=sid:eid;
    asscDet=zeros(1,F); % which detection is close by?
    widths=zeros(1,F);
    heights=zeros(1,F);
    scores=zeros(1,F);
    
    % find closest detections
    for t=frames
        ndets=length(detections(t).xp); % how many dets in this frame
        if ndets
            xy=[X(t,id); Y(t,id)];
            dets=[detections(t).xp; detections(t).yp];
        
            alldist=sqrt(sum((repmat(xy,1,ndets)-dets).^2)); % distance to all        
            [mindist, mindet]=min(alldist);
            if mindist<=sceneInfo.targetSize
                asscDet(t)=mindet;
                widths(t)=detections(t).wd(mindet);
                heights(t)=detections(t).ht(mindet);
                scores(t)=detections(t).sc(mindet);
            end
        end        
    end        
    detsAssc=find(asscDet); % which detections associated
    detsAsscWobble=detsAssc;%+0.01*rand(1,length(t))-0.005; % add random noise to avoid NaN in fitting (LOOK INTO THIS!)    
    
    if numel(unique(detsAssc))>1
    polydeg=min(9,max(1,floor(numel(detsAssc)/100)));
    polystr=sprintf('poly%d',polydeg);
    sp=splinefit(detsAsscWobble, heights(detsAssc),1,max(1,floor(numel(detsAssc)/100))+1,'r',scores(detsAssc));
    ipolheights=ppval(sp,frames);
    
    
    H((sid:eid)',id)=ipolheights';
    
    if ~isfield(sceneInfo,'targetAR') % if no aspect ratio given, estimate widths        
        sp=splinefit(detsAsscWobble, widths(detsAssc),1,max(1,floor(numel(detsAssc)/100))+1,'r',scores(detsAssc));
        ipolwidths = ppval(sp,frames);
        W((sid:eid)',id)=ipolwidths';
    end
    
    else % strange trajectory with < 3 detections
        detwidthmean=[]; detheightmean=[];
        for t=sid:eid
            detwidthmean=[detwidthmean mean(detections(t).wd)];
            detheightmean=[detheightmean mean(detections(t).ht)];
        end
        detwidthmean(isnan(detwidthmean))=mean(detwidthmean(~isnan(detwidthmean)));
        detheightmean(isnan(detheightmean))=mean(detheightmean(~isnan(detheightmean)));
        W((sid:eid)',id)=detwidthmean;
        H((sid:eid)',id)=detheightmean;
    end
          
end

% if we have camera calibration
% lets assume all people are 1.7m tall and push
% the heights of bboxes towards that value
if isfield(sceneInfo,'camPar')
    heightPrior=getHeightPrior(stateInfo);
    prwght=.8;
    H=(1-prwght)*H + prwght*heightPrior;   
    
end



% aspectRatio= 1/2;
% aspectRatio= 1/3;
% aspectRatio=1;

% normalize ratio to dataset mean?
if sceneInfo.gtAvailable
    global gtInfo
    arithmean=mean(gtInfo.W(~~gtInfo.W)./gtInfo.H(~~gtInfo.H));    
    aspectRatio= arithmean; 
end

stateInfo.H=H;

% at least 30 pixels heigh
stateInfo.H(stateInfo.H<30)=30;


% if aspect ratio provided by user, take it
if isfield(sceneInfo,'targetAR')
    stateInfo.W=H*sceneInfo.targetAR;
else
    stateInfo.W=W;
end


% at least 15 pixels wide
stateInfo.W(stateInfo.W<15)=15;

% clean up mess
stateInfo.W(~X)=0; stateInfo.H(~X)=0;

% WTF?
% isnanH=find(isnan(stateInfo.H));
% isnumH=setdiff(find(stateInfo.H),isnanH);
% stateInfo.H(isnanH)=mean(stateInfo.H(isnumH));
% isnanW=find(isnan(stateInfo.W));
% isnumW=setdiff(find(stateInfo.W),isnanW);
% stateInfo.W(isnanW)=mean(stateInfo.W(isnumW));


    

end