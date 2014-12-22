function [envelope_data] = envelope(train_label, train_data, test_data, num_std)
%==========================================================================
% Inputs:
% train_label           [m x 1] : label for training data
% train_data			[m x p] : training data for sequences
% test_data				[n x p] : testing data for sequences
% num_std				[k] 	: number of standard deviations  
%--------------------------------------------------------------------------
% Outputs:
% envelope_data			[n x ?] : represent testing data with envelope
%==========================================================================
    % Get unique label
    unique_label = unique(train_label);
	
	% Get dimensions
    s_train = size(train_data);
    s_test = size(test_data);
    s_label = size(unique_label);
	
    % Initial mean and std array
    mean_train = zeros(s_label(1), s_train(2));
    std_train = zeros(s_label(1), s_train(2));

	% Compute mean and std separately
    for count=1:s_label(1)
        label = unique_label(count);
        mean_train(count, :) = mean(train_data(train_label==label, :));
        std_train(count, :) = std(train_data(train_label==label, :));
    end
    size(mean_train)
	% Initial envelope data
    datalen = 8;
    envelope_data = zeros(s_test(1), datalen*s_label(1));
	max = 32767;
    
    for i=1:s_test(1)
        for count=1:s_label(1)
            % Sum of value which is over N * std  
            upper_index = find((test_data(i, :)>(mean_train(count, :)+num_std*std_train(count, :))) == 1);
            lower_index = find((test_data(i, :)<(mean_train(count, :)-num_std*std_train(count, :))) == 1);
           
            overupper = 0;
            overlower = 0;
     
            if size(upper_index, 2) > 0
                overupper = sum(abs(test_data(i, upper_index)));
            end
            
            if size(lower_index, 2) > 0
                overlower = sum(abs(test_data(i, lower_index)));
            end
            
            % Get nearly 8 points at 20% point to vote 
            num_one_20_per = sum(test_data(i, round(s_test(2)*0.2)-4:round(s_test(2)*0.2)+4)>mean_train(count, round(s_test(2)*0.2)-4:round(s_test(2)*0.2)+4)+num_std*std_train(count, round(s_test(2)*0.2)-4:round(s_test(2)*0.2)+4));
            num_mone_20_per = sum(test_data(i, round(s_test(2)*0.2)-4:round(s_test(2)*0.2)+4)>mean_train(count, round(s_test(2)*0.2)-4:round(s_test(2)*0.2)+4)+num_std*std_train(count, round(s_test(2)*0.2)-4:round(s_test(2)*0.2)+4));
            num_fit_20_per = 8 - num_one_20_per - num_mone_20_per;
            % voting
            if num_one_20_per > 2 
                per_20_position = 1;
            elseif num_mone_20_per > 2
                per_20_position = -1;
            elseif num_fit_20_per > 2
                per_20_position = 0;
            end
               
            % Get nearly 8 points at 50% point to vote 
            num_one_50_per = sum(test_data(i, round(s_test(2)*0.5)-4:round(s_test(2)*0.5)+4)>mean_train(count, round(s_test(2)*0.5)-4:round(s_test(2)*0.5)+4)+num_std*std_train(count, round(s_test(2)*0.5)-4:round(s_test(2)*0.5)+4));
            num_mone_50_per = sum(test_data(i, round(s_test(2)*0.5)-4:round(s_test(2)*0.5)+4)>mean_train(count, round(s_test(2)*0.5)-4:round(s_test(2)*0.5)+4)+num_std*std_train(count, round(s_test(2)*0.5)-4:round(s_test(2)*0.5)+4));
            num_fit_50_per = 8 - num_one_50_per - num_mone_50_per;
            if num_one_50_per > 2 
                per_50_position = 1;
            
            elseif num_mone_50_per > 2
                per_50_position = -1;
            
            elseif num_fit_50_per > 2
                per_50_position = 0;
            end
            
            % Get nearly 8 points at 80% point to vote 
            num_one_80_per = sum(test_data(i, round(s_test(2)*0.8)-4:round(s_test(2)*0.8)+4)>mean_train(count, round(s_test(2)*0.8)-4:round(s_test(2)*0.8)+4)+num_std*std_train(count, round(s_test(2)*0.8)-4:round(s_test(2)*0.8)+4));
            num_mone_80_per = sum(test_data(i, round(s_test(2)*0.8)-4:round(s_test(2)*0.8)+4)>mean_train(count, round(s_test(2)*0.8)-4:round(s_test(2)*0.8)+4)+num_std*std_train(count, round(s_test(2)*0.8)-4:round(s_test(2)*0.8)+4));
            num_fit_80_per = 8 - num_one_80_per - num_mone_80_per;
            % voting
            if num_one_80_per > 2 
                per_80_position = 1;

            elseif num_mone_50_per > 2
                per_80_position = -1;

            elseif num_fit_50_per > 2
                per_80_position = 0;
            end
            
            
            num_one = sum(test_data(i, :)>(mean_train(count, :)+num_std*std_train(count, :)));      
            num_mone = sum(test_data(i, :)<(mean_train(count, :)-num_std*std_train(count, :)));
            
            envelope_data(i, (count-1)*datalen+1) = s_test(2)-num_one-num_mone;                                %(0)
            envelope_data(i, (count-1)*datalen+2) = num_one;                                                                 %(1)
            envelope_data(i, (count-1)*datalen+3) = num_mone;                                                             %(-1)
            envelope_data(i, (count-1)*datalen+4) = overupper/max;
            envelope_data(i, (count-1)*datalen+5) = overlower/max;
            envelope_data(i, (count-1)*datalen+6) = per_20_position;
            envelope_data(i, (count-1)*datalen+7) = per_50_position;
            envelope_data(i, (count-1)*datalen+8) = per_80_position;
            
        end
    end
end
