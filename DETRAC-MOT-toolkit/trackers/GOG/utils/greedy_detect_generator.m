function dres = greedy_detect_generator(baselinedetections, numFrames)

detections = parseDetections(baselinedetections, numFrames); 

count = 1;
for i = numFrames
    numTargets = size(detections(i).xi, 2);
    for j = 1:numTargets
        dres.w(count,1) = detections(i).wd(1,j);
        dres.h(count,1) = detections(i).ht(1,j);
        w = dres.w(count,1);
        h = dres.h(count,1);
        dres.x(count,1) = detections(i).xi(1,j) - 0.5*w;
        dres.y(count,1) = detections(i).yi(1,j) - h;
        dres.fr(count,1) = i;
        dres.r(count,1) = detections(i).sc(1,j)*3-1.5;        
        count = count+1;
    end
end

dres = build_graph(dres);