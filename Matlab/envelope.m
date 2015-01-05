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
        std_train(count, :)  = std(train_data(train_label==label, :));
    end

    size(mean_train)
	% Initial envelope data
    datalen = 3;
    envelope_data = zeros(s_test(1), datalen*s_label(1));
            
            num_one = sum(test_data(i, :)>(mean_train(count, :)+num_std*std_train(count, :)));      
            num_mone = sum(test_data(i, :)<(mean_train(count, :)-num_std*std_train(count, :)));
            
            envelope_data(i, (count-1)*datalen+1) = s_test(2)-num_one-num_mone;                                %(0)
            envelope_data(i, (count-1)*datalen+2) = num_one;                                                                 %(1)
            envelope_data(i, (count-1)*datalen+3) = num_mone;                                                             %(-1)
        end
    end
end
