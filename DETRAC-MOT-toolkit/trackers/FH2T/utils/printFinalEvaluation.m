function printFinalEvaluation(res_path, res_mat_name, cutgtFile, frame_end)

% load gtInfo
load(cutgtFile);
% load stateInfo
left = load([res_path res_mat_name '_LX.txt']);
top = load([res_path res_mat_name '_LY.txt']);
right = load([res_path res_mat_name '_RX.txt']);
down = load([res_path res_mat_name '_RY.txt']);
stateInfo = [];
h = down - top;
w = right - left;
xc = left + w/2;
yc = top + h/2;
% foot position
stateInfo.X = xc;       
stateInfo.Y = yc+h/2;
stateInfo.H = h;
stateInfo.W = w;
stateInfo.F = frame_end;
stateInfo.frameNums = 1:frame_end;
stateInfo.Xgp = stateInfo.X;
stateInfo.Ygp = stateInfo.Y;
stateInfo.Xi = stateInfo.X;
stateInfo.Yi = stateInfo.Y;

% print result
printMessage(1,'\nEvaluation 2D:\n');
[metrics, metricsInfo]=CLEAR_MOT(gtInfo,stateInfo);
printMetrics(metrics,metricsInfo,1);   
