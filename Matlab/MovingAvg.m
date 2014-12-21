function m_series=movingAvg(s,n)
    if(nargin<2)
       n=5; 
    end
    
    temp_series=0;
     m_series=zeros(size(s,1),size(s,2)-(n-1));

    for index=1:size(s,1)
        for i=1:size(s,2)-n+1
            temp_series=[temp_series mean(s(index,i:i+(n-1)))];
        end
        m_series(index,:)=temp_series;

        temp_series=0;
    end

end
