function [stateInfo, speed] = run_tracker(curSequence, baselinedetections)
% parameters
minCarWidth = 5;
minCarHeight = 5;
segSize = [10,4];
nTry = 3;

%% multi-object tracking
frameNums = curSequence.frameNums;
% create list file
listPath = 'imagelist.txt';
fidlist = fopen(listPath, 'w');
partsID = ismember(curSequence.imgFolder, '\');
id = find(partsID==1);
newFolder = [];
for i = 1:length(id)
    if(i == 1)
        staId = 1;
        endId = id(i)-1;
    else
        staId = id(i-1)+1;
        endId = id(i)-1;
    end
    newFolder = cat(2, newFolder, cat(2, curSequence.imgFolder(staId:endId), '\\'));
end
for k = frameNums
    fprintf(fidlist,[newFolder curSequence.imgFileFormat '\n'], k);
end
fclose(fidlist);                 
% configuration
fileIn = 'GraphMultiCarTracker_Config.txt';
fileOut = 'Config.txt';
fidin = fopen(fileIn,'r');
fidout = fopen(fileOut,'w'); 
nline = 0;  
while(~feof(fidin)) 
    tline = fgetl(fidin);
    nline = nline+1; 
    % change the parameter
    if(nline == 8)
        tline_ = curSequence.seqName;
        fprintf(fidout,'%s\n', tline_);
    elseif(nline == 14)
        detPath = 'detections.txt'; % detection file          
        baselinedetections(:,5) = baselinedetections(:,5) + baselinedetections(:,3);
        baselinedetections(:,6) = baselinedetections(:,6) + baselinedetections(:,4);        
        dlmwrite(detPath, baselinedetections);
        tline_ = detPath;
        fprintf(fidout,'%s\n', tline_);   
    elseif(nline == 29)
        tline_ = num2str(numel(frameNums));
        fprintf(fidout,'%s\n', tline_);    
    elseif(nline == 32)
        tline_ = num2str(minCarWidth);
        fprintf(fidout,'%s\n', tline_);  
    elseif(nline == 35)
        tline_ = num2str(minCarHeight);
        fprintf(fidout,'%s\n', tline_);                           
    elseif(nline == 38)
        tline_ = [num2str(segSize(1)) ',' num2str(segSize(2))];
        fprintf(fidout,'%s\n', tline_);  
    elseif(nline == 41)
        tline_ = num2str(nTry);
        fprintf(fidout,'%s\n', tline_);                          
    else
        fprintf(fidout,'%s\n', tline); 
    end
end
fclose(fidin);           
fclose(fidout);   
% run the tracker
if verLessThan('matlab', '7.14.0')
    [status, output] = system('GraphMultiCarTracker.exe Config.txt');
else
    [status, output] = system('GraphMultiCarTracker.exe Config.txt', '');
end

% save tracking results
stateInfo = [];                
stateInfo.F = numel(curSequence.frameNums);
stateInfo.frameNums = curSequence.frameNums;
seqID = curSequence.seqName;
if(exist(['result\' seqID '_LX.txt'],'file'))
    X = load(['result\' seqID '_LX.txt']);
    Y = load(['result\' seqID '_LY.txt']);
    W = load(['result\' seqID '_RX.txt']) - X;
    H = load(['result\' seqID '_RY.txt']) - Y;
    speed = load(['result\' seqID '_speed.txt']);      
    xc = X + W/2;
    yc = Y + H/2;
    % foot position
    stateInfo.X = xc;       
    stateInfo.Y = yc+H/2;
    stateInfo.H = W;
    stateInfo.W = H;
    stateInfo.Xgp = stateInfo.X;
    stateInfo.Ygp = stateInfo.Y;
    stateInfo.Xi = stateInfo.X;
    stateInfo.Yi = stateInfo.Y;    
else
    stateInfo.X = [];       
    stateInfo.Y = [];
    stateInfo.H = [];
    stateInfo.W = [];             
    stateInfo.Xgp = stateInfo.X;
    stateInfo.Ygp = stateInfo.Y;
    stateInfo.Xi = stateInfo.X;
    stateInfo.Yi = stateInfo.Y;                       
    speed = 0;
end
% delete the temp files
delete('result\*.txt');
delete('detections.txt');