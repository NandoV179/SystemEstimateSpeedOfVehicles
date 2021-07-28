function detections = loadDetections(detFile)

if(~exist(detFile, 'file'))
    error('no detection files');
else
    detections = load(detFile);      
end