this code solves the famous magic square problem using genetics

#Data Representation

I have used 1D array to represent each member of the population with a length of N^2, So my reconciliations and mutations are arrangement algorithms. 

#Population Selection

I used 3 ways of population selection. 
1. Directly select members with maximum fitnesses. 
2. Using probability distribution to select members by their fitnesses. 
3. Using somewhat a ranking technique. 

The first 2 techniques resulted in premature convergence of the population towards local optimums, But the 3rd technique seemed to retain diversity. Consequently, all following tests are done using the ranking algorithm. 

#Fitness evaluation 

cost of each member is calculated by summing over each of its rows, columns and diagonals, then subtracting them from the expected magic square summation. Note that the subtraction is done in absolute form so each cost element is a positive number. 
Fitness = 1 / (cost + 1) 
1 is added to cost to avoid zero value in denominator 

#Premature stop 

If the fitnesses stay constant for a 3 generations, the search will stop proceeding. Using proper mutation and reconciliation probabilities, this shall not happen. However, for small squares the risk of premature stop arises. 

#Reconciliation 

I used 2 reconciliation methods. 
1. PMX 
2. Cycle 

#Mutation 

I used 4 methods for this. 
1. Swap 
2. Insert 
3. Scramble 
4. Inversion 

#INPUT/OUTPUT

input is given by an input.txt file. Each line number contains as follows:

1. n (n^2 is the size of the magic square)
2. generation count
3. probability of reconciliation
4. probability of mutation
5. population size

an output.txt file is created upon running the code. it demonstrates the fitnesses of every generation. also it gives the best fitness for the current generation and the best fitness acheived in all the generations so far.

this work is done by Yara M. Bahram.
