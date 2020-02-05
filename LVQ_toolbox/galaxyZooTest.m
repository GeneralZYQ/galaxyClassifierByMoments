%This script is used to train with GMLVQ

E20 = load('ellipticnoidentity20.mat'); %1~202
S20 = load('spiralsnoidentity20.mat'); %1 ~278
E20Balanced = E20.EllipticsNoIdentitycombine20featureSpectrum(1:end, :);
S20Balanced = S20.SpiralsNoIdentitycombine20featureSpectrum(1:202,:);




testresultHere = (1:9);
trainresultHere = (1:9);
for n = 2:2%10
    
    sumTESTERROR = 0;
    sumTRAINERROR = 0;
    
    for x = 1:1%3

        prototypesPerClass = n;
        ellipticTrainingNum = 160;
        spiralTrainingNum = 160;
        
        my_indices = randperm(202);
        
        FirstTrainIndices = my_indices(1:ellipticTrainingNum);
        SecondTrainIndices = my_indices(1:spiralTrainingNum);
        FirstTestIndices = my_indices(ellipticTrainingNum + 1:end);
        SecondTestIndices = my_indices(spiralTrainingNum + 1:end);


        firstTr = E20Balanced(FirstTrainIndices,:); %giao1
        secondTr = S20Balanced(SecondTrainIndices, :);%giao1


        firstLabels = 1.* ones(size(firstTr,1),1);
        secondLabels = 2.* ones(size(secondTr,1),1);

        TrainSet = [firstTr; secondTr]; % Training Set
        TrainLabels = [firstLabels; secondLabels];  % Training Labels

        FirstTest = E20Balanced(FirstTestIndices,:); %giao2
        SecondTest = S20Balanced(SecondTestIndices, :); %giao2
        firstTestLabels = 1.* ones(size(FirstTest, 1),1);
        secondTestLabels =  2.* ones(size(SecondTest, 1),1);

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
        
       
        figure(1);
        imagesc(GMLVQ_model.omega'*GMLVQ_model.omega)
        title('GMLVQ: relevance matrix Lambda');colorbar;
        
        figure(2)
        bar(svd(GMLVQ_model.omega'*GMLVQ_model.omega));
        title('GMLVQ: eigenvalues of the matrix');
        
        figure(3)
        relev = GMLVQ_model.omega'*GMLVQ_model.omega;
        diagnol = diag(relev);
        ga = sum(diag(relev));
        bar(diag(relev))
        [B, I] = maxk(diagnol, 20)
        xlabel('feature')
        ylabel('lambda')
        title('GMLVQ: diagnol');
          
        
        XV = {}
        for w = 1:20
            index = I(w);
            momentIndex = mod(index, 7);
            innerIndex = (index - momentIndex) / 7;
            xStr = ['moment' num2str(momentIndex + 1) '-' num2str(innerIndex + 1)];
            XV{end + 1} = xStr;
        end
        
        Xt = categorical(XV);
        Xt = reordercats(Xt,XV);
        figure(4)
        bar(Xt,B)
        xlabel('feature name')
        ylabel('lambda')
        title('20 Features with top weights');
      
        
        sumTESTERROR = sumTESTERROR + testError;
        sumTRAINERROR = sumTRAINERROR + trainError;
    end
    
    aver1 = sumTESTERROR / 3.0;
    aver2 = sumTRAINERROR / 3.0;
    
    testresultHere(1, n -1) = aver1;
    trainresultHere(1, n - 1) = aver2;

end

%%

%{

E50 = load('elliptic50.mat'); % 3~204
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

%}


