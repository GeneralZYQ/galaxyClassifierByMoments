%This script is used to train with GMLVQ

E20 = load('elliptics20.mat'); %3~204
S20 = load('spiral20.mat'); %3 ~281

prototypesPerClass = 5;

disp(class(E20.Elliptics20Spectrum(3:30,:)));

firstTr = E20.Elliptics20Spectrum(3:160,:);
secondTr = S20.Spirals20Spectrum(3:200, :);

disp(length(firstTr));

firstLabels = 1.* ones(length(firstTr),1);
secondLabels = 2.* ones(length(secondTr),1);

TrainSet = [firstTr; secondTr]; % Training Set
TrainLabels = [firstLabels; secondLabels];  % Training Labels

FirstTest = E20.Elliptics20Spectrum(161:end,:);
SecondTest = S20.Spirals20Spectrum(201:end, :);
firstTestLabels = 1.* ones(length(FirstTest),1);
secondTestLabels =  2.* ones(length(SecondTest),1);

TestSet = [FirstTest; SecondTest];
TestLabels = [firstTestLabels; secondTestLabels];

GMLVQ_results = struct('GMLVQ_model',{},'GMLVQ_setting',{},'zscore_model',{},'trainError',{},'testError',{});
projectionDimension = size(TrainSet,2);
GMLVQparams = struct('PrototypesPerClass',prototypesPerClass,'dim',projectionDimension,'regularization',0);
[GMLVQ_model,GMLVQ_settting] = GMLVQ_train(TrainSet, TrainLabels,'dim',GMLVQparams.dim,'PrototypesPerClass',GMLVQparams.PrototypesPerClass,'regularization',GMLVQparams.regularization);

estimatedTrainLabels = GMLVQ_classify(TrainSet, GMLVQ_model);
trainError = mean( TrainLabels ~= estimatedTrainLabels );

estimatedTestLabels = GMLVQ_classify(TestSet, GMLVQ_model);
testError = mean( TestLabels ~= estimatedTestLabels );

%%

E50 = load('elliptics50.mat'); % 3~204
S50 = load('spiral50.mat'); %3 ~~ 280

first50Tr = E50.Elliptics50Spectrum(3:160,:);
second50Tr = S50.Spirals50Spectrum(3:200, :);

firstLabels = 1.* ones(length(first50Tr),1);
secondLabels = 2.* ones(length(second50Tr),1);

sTrainSet = [first50Tr; second50Tr]; % Training Set
sTrainLabels = [firstLabels; secondLabels];  % Training Labels

sFirstTest = E50.Elliptics50Spectrum(161:end,:);
sSecondTest = S50.Spirals50Spectrum(201:end, :);
sfirstTestLabels = 1.* ones(size(sFirstTest, 1),1);
ssecondTestLabels =  2.* ones(size(sSecondTest, 1),1);

sTestSet = [sFirstTest; sSecondTest];
sTestLabels = [sfirstTestLabels; ssecondTestLabels];

GMLVQ_results2 = struct('GMLVQ_model',{},'GMLVQ_setting',{},'zscore_model',{},'trainError',{},'testError',{});
projectionDimension2 = size(sTrainSet,2);

GMLVQparams2 = struct('PrototypesPerClass',prototypesPerClass,'dim',projectionDimension2,'regularization',0);
[GMLVQ_model2,GMLVQ_settting2] = GMLVQ_train(sTrainSet, sTrainLabels,'dim',GMLVQparams2.dim,'PrototypesPerClass',GMLVQparams2.PrototypesPerClass,'regularization',GMLVQparams2.regularization);

estimatedTrainLabels2 = GMLVQ_classify(sTrainSet, GMLVQ_model2);
trainError2 = mean( sTrainLabels ~= estimatedTrainLabels2 );

disp(size(sTestSet, 1))
disp(size(sTestLabels, 1))


estimatedTestLabels2 = GMLVQ_classify(sTestSet, GMLVQ_model2);
testError2 = mean( sTestLabels ~= estimatedTestLabels2 );


