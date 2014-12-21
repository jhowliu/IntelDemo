function [ vectorFeature ] = Vectorization2( seriesData )
%
% Vectorization     
% 
% Programmer: Jing-Yao Lin      
%                                                                   
% Inputs                                                            
%   seriesData: NxM matrix of time series                                      
%      N is number of instance                                      
%      M is length of time series                                       
%                                                                   
% Outputs                                                           
%   vectorFeature: each time series will be represented as vector
% Note                                                              
%   each value in output abof was normalized to [0, 1]              
%
    dataLength = length(seriesData(1,:));
% 1) to 3) min, max, mean.    
    tsMin = min(seriesData,[],2);
    tsMax = max(seriesData,[],2);
    tsMean = mean(seriesData,2);
    
    vectorFeature(:,1) = tsMin;
    vectorFeature(:,2) = tsMax;
    vectorFeature(:,3) = tsMean;
%     vectorFeature(:,4) = tsSTD;
% % % % % % % % % % % % % % % % % % % % % % % % % % % % % %   
% 4) and 5) number of peaks and valleys
% 6) and 7) mean of peak and valley values
% 8) and 9) mean of interval between peaks and valley
% find peak and valley locations, which include start and end point
    velocitySeriesData = seriesData(:,2:end)-seriesData(:,1:end-1);
    velocitySeriesDataBoolean = ones(size(velocitySeriesData));
    velocitySeriesDataBoolean(velocitySeriesData>=1)=1;
    velocitySeriesDataBoolean(velocitySeriesData<1)=-1;
    trendDirection = velocitySeriesDataBoolean(:,2:end)+velocitySeriesDataBoolean(:,1:end-1);
    [turnPointLocation(:,1),turnPointLocation(:,2)] = find(trendDirection==0);
    turnPointLocation(:,2)=turnPointLocation(:,2)+1;    
    linearInd = sub2ind(size(velocitySeriesDataBoolean), turnPointLocation(:,1), turnPointLocation(:,2));
    trendValue = velocitySeriesDataBoolean(linearInd);
    tempIndic = find(trendValue<0);
    peakLocation = [turnPointLocation(tempIndic,1),turnPointLocation(tempIndic,2)];
    tempIndic = find(trendValue>0);
    valleyLocation = [turnPointLocation(tempIndic,1),turnPointLocation(tempIndic,2)];
%  to compute features of each sample of time series
    for i = 1: size(seriesData,1)        
        
        nowPeaksIndic=[1;peakLocation(peakLocation(:,1)==i,2);size(seriesData,2)];
        nowValleysIndic=[1;valleyLocation(valleyLocation(:,1)==i,2);size(seriesData,2)];   
        vectorFeature(i,4) = length(nowPeaksIndic);
        vectorFeature(i,5) = length(nowValleysIndic);
        vectorFeature(i,6) = mean(seriesData(i,nowPeaksIndic));
        vectorFeature(i,7) = mean(seriesData(i,nowValleysIndic));
        vectorFeature(i,8) = mean(nowPeaksIndic(2:end)-nowPeaksIndic(1:end-1));
        vectorFeature(i,9) = mean(nowValleysIndic(2:end)-nowValleysIndic(1:end-1));
        
    end
 % 10) first sensor reading of each time series
 % 11) median of first 10% data points
 % 12) to 16) mean of 5 equal parts of time series
 % 17) summarization of absolute value of changes in amplitude reading of timestamps

    vectorFeature(:,10) = seriesData(:,1);    
    vectorFeature(:,11) = median(seriesData(:,1:floor(end*0.10)),2);
    segLength = dataLength/5;
    nowNumberOfVector = size(vectorFeature,2);
    for i = 1:5
        vectorFeature(:,nowNumberOfVector+i)=mean(seriesData(:,floor(segLength*(i-1))+1:floor(segLength*i)),2);
    end

    
    vectorFeature(:,17) = sum(abs(velocitySeriesData),2);

    
end

