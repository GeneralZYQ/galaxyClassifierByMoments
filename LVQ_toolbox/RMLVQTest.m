
ind = 2;
fid = fopen('moments.csv');

myline = fgetl(fid);
firstElements = strsplit(myline, ',');
firstVec(1,:) = firstElements;
while ischar(myline)
    C = strsplit(myline,',');
    % C now contains a cell array for each line, maybe you can work with that?
    firstVec(ind, :) = C;
    myline = fgetl(fid);
    ind = ind + 1;
end
fclose(fid);

trainData = firstVec(:,3:9);
trainLabels = firstVec(:,2);
xTrainData = str2double(trainData);
disp (size(trainLabels,1))

xTrainLab = [];

for ii = 1:87 
    val = trainLabels(ii,1);
    xTrainLab(ii, 1) = 1;
    if strcmp(val, 'Ellipticals')
        xTrainLab(ii, 1) = 1;
    end
    
    if strcmp(val, 'barrdSpiral')
        xTrainLab(ii, 1) = 2;
    end
    
    if strcmp(val, 'Spiral')
        xTrainLab(ii, 1) = 3;
    end
    
    if strcmp(val, 'Irregular')
        xTrainLab(ii, 1) = 4;
    end
    
end

disp(isnumeric(xTrainLab))

TrainDataIndices = []
TestDataIndices = []


for ii = 1:7
    s = RandStream('mlfg6331_64');
    testIndices = datasample(s,1:87,12,'Replace',false);
    TestDataIndices(ii, :) =testIndices;
    TrainDataIndices(ii, :) =setdiff(1:87, testIndices);
end

% ar = xTrainData(1, combos(1,:));
% disp(ar)

for pick = 1:7
    combos = nchoosek(1:7,pick);
    for pickth = 1:size(combos,1)
        moments = combos(pickth, :);
        for trainIndiceisth = 1:size(TrainDataIndices, 1)
            subTrainData = xTrainData(TrainDataIndices(trainIndiceisth, moments));
            subTrainLabel = xTrainLab(TrainDataIndices(trainIndiceisth, :));
            
            subTestData = xTrainData(TestDataIndices(trainIndiceisth, moments));
            subTestLabel = xTrainLab(TestDataIndices(trainIndiceisth, :));
        end
    end
end


p = rand(1,10);
q = ones(10);
save('pqfile.mat','p','q')


GMLVQ_model = GMLVQ_train(xTrainData, xTrainLab);




