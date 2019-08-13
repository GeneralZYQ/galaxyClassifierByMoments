MyFolderInfo = dir('D:\galaxyClassifierByMoments\spiral_50_spectrum');
L = length(MyFolderInfo);
disp(L);

Spirals50Spectrum = (1:50);

for n = 1 : L
    w = MyFolderInfo(n).name;
    fullpath = strcat('D:\galaxyClassifierByMoments\spiral_50_spectrum', '\', w);
    disp(fullpath);
    if contains(fullpath, 'spectrum.csv')
        %M = csvread(fullpath);
        
        fid = fopen(fullpath);
        myline = fgetl(fid);
        %disp(class(myline));
        a = split(myline);
        disp(a);
        ele = split(a, ',');
        eled = ele';
        for j = 1:50
            x = eled(j);
            xm = cell2mat(x);
            xfl = length(xm);
        
            finalstr = '';
            for i = 1:xfl
                finalstr = strcat(finalstr, xm(i));
            
            end
            disp(str2num(finalstr));
            Spirals50Spectrum(n, j) = str2num(finalstr);
        end
        
        
        fclose(fid);
        
       
    end
    
end

%disp(Elliptics20Spectrum)