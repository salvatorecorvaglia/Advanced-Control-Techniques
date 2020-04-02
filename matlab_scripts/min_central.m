function min_central= min_central(fx,component)
x=sym('x', [1 component]);


%fun= @(x)fx;
if ischar(fx) 
    file=fopen('/Users/simonemiglietta/Desktop/dataset/data.txt','r'); %NOTE !! this path must be the same of 'dataset generator'!
    
    A= fscanf(file,'%f %f\n')
    length(A)
    i=1
    j=1
    
    sum=@(x) 0;
    while i <=99
        x_p(j) = A(i);
        y_p(j) =A(i+1);
        j=j+1
        i=i+2;
    end
    fclose(file);
    for i=1:50
       f =@(x)((x_p(i)*x(1)+x(2)- y_p(i))^2);
       
       
      
       sum =@(x) sum(x) + f(x)
            
       %sum(i) = @(x) s(x) + sum(x);
       
    end   
    
    size=[5,5];
    [x_min fval]=fminsearch(@(x) sum(x), size)
    file=fopen('/Users/simonemiglietta/Desktop/dataset/min.txt','w'); % NOTE!! modify path! (1)
    fprintf(file,'%f',fval);

    fclose(file);
    'success'
      
    
    

else
    
    states = 10*rand(component);
    [x_min fval]=fminsearch(fx, states)
    file=fopen('/Users/simonemiglietta/Desktop/dataset/min.txt','w');   % NOTE!! modify path! same as (1)
    fprintf(file,'%f',fval);

    fclose(file);
    'success'
end