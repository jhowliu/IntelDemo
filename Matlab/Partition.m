function [axis1, axis2, axis3, axis4, axis5, axis6, pressure1, pressure2, pressure3, pressure4] = dataPartition(Data, length)

    addpath('G:\Dropbox\DM_ML\inel_project\Code')

    %  ----------------------------data partition------------------------------
     axis1=[]; axis2=[]; axis3=[]; axis4=[]; axis5=[]; axis6=[]; pressure1=[]; pressure2=[]; pressure3=[]; pressure4=[];
    index1=1; index2=1;

    for i=1:size(Data,2)-3
        for j=1:size(Data,1)
            if Data(j,i) > mean(Data(:,i))+3*std(Data(:,i))
                Data(j,i)=mean(Data(:,i))+3*std(Data(:,i));
            elseif Data(j,i) < mean(Data(:,i))-3*std(Data(:,i))
                Data(j,i)=mean(Data(:,i))-3*std(Data(:,i));
            end
        end
    end
   
    for i=2:size(Data,1)
        if Data(i,1)~=0    
          continue;
        else
            index2=i-1;
            disp([num2str(i) , ' : ' , num2str(length-10-(index2-index1+1)-3)])
            axis1=[axis1; movingAvg(Data(index1:index2,2)') zeros(1,length-(index2-index1+1)-3) ]; 
            axis2=[axis2; movingAvg(Data(index1:index2,3)') zeros(1,length-(index2-index1+1)-3) ]; 
            axis3=[axis3; movingAvg(Data(index1:index2,4)') zeros(1,length-(index2-index1+1)-3) ]; 
            axis4=[axis4; movingAvg(Data(index1:index2,5)') zeros(1,length-(index2-index1+1)-3) ]; 
            axis5=[axis5; movingAvg(Data(index1:index2,6)') zeros(1,length-(index2-index1+1)-3) ]; 
            axis6=[axis6; movingAvg(Data(index1:index2,7)') zeros(1,length-(index2-index1+1)-3) ];
            pressure1=[pressure1; movingAvg(Data(index1:index2,8)') zeros(1,length-(index2-index1+1)-3) ];
            pressure2=[pressure2; movingAvg(Data(index1:index2,9)') zeros(1,length-(index2-index1+1)-3) ];
            pressure3=[pressure3; movingAvg(Data(index1:index2,10)') zeros(1,length-(index2-index1+1)-3) ];
            pressure4=[pressure4; movingAvg(Data(index1:index2,11)') zeros(1,length-(index2-index1+1)-3) ];
            index1=i;
        end
    end

    %{
    
    sum_axis1 = [axis1Han; ones(size(axis1JY,1),1) axis1JY(:,2:end); 2*ones(size(axis1Jhow,1),1) axis1Jhow(:,2:end); 3*ones(size(axis1Rick,1),1) axis1Rick(:,2:end); 4*ones(size(axis1Song,1),1) axis1Song(:,2:end); 5*ones(size(axis1T,1),1) axis1T(:,2:end) ];
    sum_axis2 = [axis2Han; ones(size(axis2JY,1),1) axis2JY(:,2:end); 2*ones(size(axis2Jhow,1),1) axis2Jhow(:,2:end); 3*ones(size(axis2Rick,1),1) axis2Rick(:,2:end); 4*ones(size(axis2Song,1),1) axis2Song(:,2:end); 5*ones(size(axis2T,1),1) axis2T(:,2:end) ];
    sum_axis3 = [axis3Han; ones(size(axis3JY,1),1) axis3JY(:,2:end); 2*ones(size(axis3Jhow,1),1) axis3Jhow(:,2:end); 3*ones(size(axis3Rick,1),1) axis3Rick(:,2:end); 4*ones(size(axis3Song,1),1) axis3Song(:,2:end); 5*ones(size(axis3T,1),1) axis3T(:,2:end) ];
    sum_axis4 = [axis4Han; ones(size(axis4JY,1),1) axis4JY(:,2:end); 2*ones(size(axis4Jhow,1),1) axis4Jhow(:,2:end); 3*ones(size(axis4Rick,1),1) axis4Rick(:,2:end); 4*ones(size(axis4Song,1),1) axis4Song(:,2:end); 5*ones(size(axis4T,1),1) axis4T(:,2:end) ];
    sum_axis5 = [axis5Han; ones(size(axis5JY,1),1) axis5JY(:,2:end); 2*ones(size(axis5Jhow,1),1) axis5Jhow(:,2:end); 3*ones(size(axis5Rick,1),1) axis5Rick(:,2:end); 4*ones(size(axis5Song,1),1) axis5Song(:,2:end); 5*ones(size(axis5T,1),1) axis5T(:,2:end) ];
    sum_axis6 = [axis6Han; ones(size(axis6JY,1),1) axis6JY(:,2:end); 2*ones(size(axis6Jhow,1),1) axis6Jhow(:,2:end); 3*ones(size(axis6Rick,1),1) axis6Rick(:,2:end); 4*ones(size(axis6Song,1),1) axis6Song(:,2:end); 5*ones(size(axis6T,1),1) axis6T(:,2:end) ];
    sum_pressure1 = [pressure1Han; ones(size(pressure1JY,1),1) pressure1JY(:,2:end); 2*ones(size(pressure1Jhow,1),1) pressure1Jhow(:,2:end); 3*ones(size(pressure1Rick,1),1) pressure1Rick(:,2:end); 4*ones(size(pressure1Song,1),1) pressure1Song(:,2:end); 5*ones(size(pressure1T,1),1) pressure1T(:,2:end) ];
    sum_pressure2 = [pressure2Han; ones(size(pressure2JY,1),1) pressure2JY(:,2:end); 2*ones(size(pressure2Jhow,1),1) pressure2Jhow(:,2:end); 3*ones(size(pressure2Rick,1),1) pressure2Rick(:,2:end); 4*ones(size(pressure2Song,1),1) pressure2Song(:,2:end); 5*ones(size(pressure2T,1),1) pressure2T(:,2:end) ];
    sum_pressure3 = [pressure3Han; ones(size(pressure3JY,1),1) pressure3JY(:,2:end); 2*ones(size(pressure3Jhow,1),1) pressure3Jhow(:,2:end); 3*ones(size(pressure3Rick,1),1) pressure3Rick(:,2:end); 4*ones(size(pressure3Song,1),1) pressure3Song(:,2:end); 5*ones(size(pressure3T,1),1) pressure3T(:,2:end) ];
    sum_pressure4 = [pressure4Han; ones(size(pressure4JY,1),1) pressure4JY(:,2:end); 2*ones(size(pressure4Jhow,1),1) pressure4Jhow(:,2:end); 3*ones(size(pressure4Rick,1),1) pressure4Rick(:,2:end); 4*ones(size(pressure4Song,1),1) pressure4Song(:,2:end); 5*ones(size(pressure4T,1),1) pressure4T(:,2:end) ];
    %}
    
    
end


