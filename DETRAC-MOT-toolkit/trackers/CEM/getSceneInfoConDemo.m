function sceneInfo = getSceneInfoConDemo(curSequence)

sceneInfo.imgFolder = curSequence.imgFolder;
sceneInfo.frameNums = curSequence.frameNums;
sceneInfo.imgFileFormat = curSequence.imgFileFormat;

% image dimensions
sceneInfo.imgHeight = curSequence.imgHeight;
sceneInfo.imgWidth = curSequence.imgWidth;

%% tracking area
% if we are tracking on the ground plane
% we need to explicitly secify the tracking area
% otherwise image = tracking area
sceneInfo.trackingArea=[1 sceneInfo.imgWidth 1 sceneInfo.imgHeight];   % tracking area

%% camera
cameraconffile=[];
sceneInfo.camFile=cameraconffile;

%% target size
sceneInfo.targetSize=sceneInfo.imgWidth/30;

%% ground truth
sceneInfo.gtAvailable=0;