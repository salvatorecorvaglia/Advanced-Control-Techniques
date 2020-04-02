how it works?

- 1 at first run 'dataset_generator.m' to generate the dataset into a txt file called 'data.txt'. Note that you have to modify
	the path indicated in the script by entering a valid one.


- 2 (optional)  run 'min_central.m' if you want to have a comparison between the centralized and the MPI software in terms of accuracy. To run it properly you have to specify a symbolic function, so on the command window type:

	$ x=sym('x', [1 n])  % subs n with the number of components you want to work with;
	$ fun =@(x) [specify symbolic function]
	$ min_central(fun, n) % call the script specifying number of components

IMPORTANT! as the MPI software asks to enter a function or more, by entering a single function will assign it to all agents:

	i.e :  I run MPI software ('mpi_min') with 4 nodes, i decide to enter a single function 	x0^2 (in Python x0**2), (1 component, only as example).
	then:
	f(1)=x0^2
	f(2)=x0^2
	f(3)=x0^2
	f(4)=x0^2
	as the problem is formulated (see paper), this is equivalent to minimize a function that 	is the sum of f(i), in this case ,

	f(1)+f(2)+f(3)+f(4)=   4*x0^2 

	so to have a correct comparison between centralized and distributed, i have to enter 		4*x0^2 as function to minimize in 'min_central.m' :

	$ x=sym('x', [1 n])
	$ fun =@(x) 4*x(1)^2       % (Matlab indexes start from 1 )
	$ min_central(fun, 1)

	the result will be saved on a file called 'min.txt' and will be used as comparison term 	in the MPI software.

	If you want to minimize the 'big' least square function instead , simply do this:

	$ x=sym('x', [1 2]) 
	$ min_central('', 2)  % the software will read the dataset and compute the cost function 			      % entirely


-3 run 'mpi_min.py' by Python terminal with :
	$ mpiexec -n N python mpi_min.py    % where N is the number of nodes and has to be 						    % specified in the command

	then follow the requests of the code; see documentation or code comments in case of 
	misunderstandings. At the end there will be consensus plot and if 'min_central.m' has 		been run before correctly, on the file 'Comparison.png' will be plotted the difference 		between central and MPI minimum value.



-4 (otional) run 'exec_proj.m' our first software that computes the minimum of given functions f:R-> R.
	On command window type:
	$ syms x
	$ fun = [f(1),..., f(n)]  % enter NN functions (one for each agent) in x variable. By 					  % default NN = 5 (manually settable)
	$ exec_proj(fun)


-5 (optional)  run 'solver_min.py' as Python script for the 'simulating distributed' version of 'mpi_min.py'; it simulate nodes with a 'for cycle'.









