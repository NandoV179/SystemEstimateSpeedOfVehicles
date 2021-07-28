function run_experiment()

global options
    
%% evaluation for detection
if(strcmp(options.evaluateType, 'Detection'))   
    disp('**************************EVALUATION FOR DETECTION**************************');
    detectionEvaluation();
end

%% evaluation for tracking
if(strcmp(options.evaluateType, 'Tracking'))
    disp('**************************EVALUATION FOR TRACKING***************************');    
    trackingEvaluation();
end