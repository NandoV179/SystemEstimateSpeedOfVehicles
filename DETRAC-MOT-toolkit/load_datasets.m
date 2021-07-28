function sequences = load_datasets()

global options

fidSeq = importdata(options.seqPath);
sequences = cell(1, length(fidSeq));
for idSeq = 1:length(fidSeq)
    % sequence name
    seqName = fidSeq{idSeq};
    % load images
    sequences{idSeq}.seqName = seqName;
    sequences{idSeq}.imgFolder = [options.imgPath  seqName '\'];
    sequences{idSeq}.imgFileFormat = 'img%05d.jpg';
    sequences{idSeq}.dataset = dir([sequences{idSeq}.imgFolder '*.jpg']); % the folder in which ur images exists
    if(isempty(sequences{idSeq}.dataset))
    	error('error in loading images!');
    end
    sequences{idSeq}.frameNums = 1:length(sequences{idSeq}.dataset);
    [sequences{idSeq}.imgHeight, sequences{idSeq}.imgWidth, ~] = size(imread([sequences{idSeq}.imgFolder,sprintf(sequences{idSeq}.imgFileFormat,sequences{idSeq}.frameNums(1))]));    
    sequences{idSeq}.camFile = [];
    % load groundtruth
    sequences{idSeq}.gtFolder = options.gtPath;
    if(~strcmp(options.evaluateSeqs, {'DETRAC-Test', 'DETRAC-Test-Beginner', 'DETRAC-Test-Experienced'}))
        sequences{idSeq}.gtInfo = parseGT([sequences{idSeq}.gtFolder seqName '.xml'], sequences{idSeq}.imgHeight, sequences{idSeq}.imgWidth, sequences{idSeq}.frameNums);  
    else
        sequences{idSeq}.gtInfo = [];
    end
    % load ignore regions
    sequences{idSeq}.ignoreRegion = load(['evaluation/igrs/' seqName '_IgR.txt']);
end