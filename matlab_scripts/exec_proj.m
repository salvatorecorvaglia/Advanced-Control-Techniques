
function G= exec_proj(func)


NN = 5; %numero di agenti

%== Adjancency Matrix ==%
while 1
    Adj = binornd(1,0.2,NN,NN); % which entry is 1 with prob 0.2
    v=ones(1,NN-1);
    Adj = or(Adj,Adj'); % symmetrize - undirected
    I_NN = eye(NN);
    Adj = or(Adj,I_NN); % add self-loops
    
    testAdj = (I_NN+Adj)^NN; % check if G is connected
     
    if ~any(any(~testAdj))
     fprintf('\nthe graph is connected.\n');
     break;
    else
        fprintf('\nthe graph is disconnected.\n');
    end
end

if 0 % %* Row Stochastic weights *%
    WW = zeros(size(Adj));
    for ii = 1:NN
        WW(ii,:) = Adj(ii,:)./sum(Adj(ii, :));
    end
    
    WW*ones(NN, 1) - ones(NN,1)
    ones(NN, 1)'*WW - ones(NN,1)'
   % pause
end
if 1%** Doubly stochastic matrix **%
  % Degree matrix
  DEGREE = diag(sum(Adj));
  % Compute the Laplacian
  Lapl = DEGREE - Adj;
  WW = I_NN - 0.05*Lapl;  

  % Test
  WW*ones(NN,1)  - ones(NN,1)   % row stoch?
  ones(NN,1)'*WW - ones(NN,1)'  % col stoch?
  %pause
end

MAX_ITERS = 200;
syms   x
step=0.01;
XX = zeros(NN,MAX_ITERS);

x0 = 10*rand(NN,1); % initial conditions
XX(:,1) = x0;
flag=1;
s=zeros(NN, MAX_ITERS);
for tt = 1:MAX_ITERS-1
    if ~mod(tt, 10)
        fprintf('\nIteration %d / %d\n',tt,MAX_ITERS);
    end
    
    for ii = 1:NN
        N_ii = find(Adj(ii,:)==1)'; % In-Neighbors
        
        %Neighbors of ii
        U_i2 = 0;
        U_i = 0;
        for jj = N_ii % jj \in Ni
            if (flag==1)
                for kk=1:NN
                s(kk,1)= deriv(func(kk),XX(kk,1));
                
                end
                flag=0;
            end
                % s(jj,1)= val_diff(func(jj),XX(jj,1));
                 
            
           
            U_i = U_i + WW(ii,jj)*XX(jj,tt);%- step*(s(ii,tt));
            U_i2= U_i2+WW(ii,jj)*(s(jj,tt));%+ val_diff(y,XX(ii,tt+1))-val_diff(y,XX(ii,tt));
           
        end
       
         XX(ii,tt+1) = U_i -step*(s(ii,tt));
         s(ii,tt+1)=U_i2+ deriv(func(ii),XX(ii,tt+1))-deriv(func(ii),XX(ii,tt));
       % S_i=U_i2;
    end
    s
end % end:tt
%G=graph(Adj)
%figure, plot(G)
%interval=1:tt+1;
%figure, plot(interval,XX)

XX
WW
 % x0 = XX(:,1);
[v,~] = eigs(WW',1); % Right largest, 1, eigenvalue and eigenvector

alpha = v'*x0/sum(v);

interval = 1:tt;

figure
 % plot(interval, alpha*ones(size(interval)), '-.','LineWidth',1.4);
  hold on; grid on;

  %plot(interval ,repmat(mean(x0),1,tt), '-.','LineWidth',1.4);
  plot(interval ,XX(:,1:tt), '-','LineWidth',1.4);

  xlabel('$t$','Interpreter','latex')

  ylabel('$x^{[i]}(t), i \in \{ 1, \ldots, N \}$','Interpreter','latex')

  
  set(gca,'FontSize',14)
  grid on, zoom on

end
% Compute the consensus value
