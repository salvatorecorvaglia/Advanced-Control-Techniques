
 l_b     = 0;
        u_b     = 10;
        w       = 2;
        b       = 1;
        fun     = @(x) w .* x + b;

        n_examples = 50;

        x = l_b + (u_b - l_b) * rand(n_examples, 1)
        mu = 0;
        sigma = 1.5;
        y = fun(x) + normrnd(mu, sigma, [n_examples 1])

        linear_regression_dataset = [x y];
        linear_regression_dataset([2])
        file=fopen('/Users/simonemiglietta/Desktop/dataset/data.txt','w');  %  NOTE : modify path !!
        
        
        for i=1:50
            
                fprintf(file,'%f %f\n',linear_regression_dataset(i),linear_regression_dataset(i+50));

        end
        fclose(file);
