import random

class magicSquare:
    def __init__(self, parent_count, population_count, generation_count, square_size, mutation_probability, reconciliation_probability):

        self.population_count = population_count
        self.generation_count = generation_count
        self.square_size = square_size
        self.mutation_probability = mutation_probability
        self.reconciliation_probability = reconciliation_probability
        self.parent_count = parent_count
        
        self.noChangeInCostNum = 3
        self.maxOfFitness = 0
        self.maxOfFitness_index = 0
        
        self.expectedSum = self.sumEval()
           


    def findBestValues(self):
        
        w = open('output.txt','w+')
        
        square = []   
        cost_list = []
        previous_cost_list = []
        cost_no_change_count = 0
        
        square = self.generateParents()
              
        #****************************************main loop*******************************************   
        for repeat in range(self.generation_count):
            #cost for each parent
            cost_list.clear()
            for x in square:
                cost_list.append(self.cost(x))
           
            print("***************************************************")    
            print("***************************************************")   
            print("initial squares")    
            print(square)
            print("\ninitial fitnesses")   
            print(cost_list) 
            print("\n***************************************************")   
            
            #_______________________________________using min(cost)______________________________________          
            #choose the best parents to repopulate 
#            while len(cost_list) > self.population_count:
#                index_of_max = cost_list.index(min(cost_list))
#                square.pop(index_of_max)
#                cost_list.pop(index_of_max)

            #_______________________________________using probability distribution________________________
            square = random.choices(population=square, weights=rankify_improved(cost_list), k=self.population_count)
            
            #_____________________________________________________________________________________________  
    
    
            #cost list for the chosen children
            cost_list.clear()
            for x in square:
                cost_list.append(self.cost(x))
                
            if max([max(cost_list), self.maxOfFitness]) == max(cost_list) and self.maxOfFitness != max(cost_list):
                self.maxOfFitness = max([max(cost_list), self.maxOfFitness]) 
                self.maxOfFitness_index = repeat
            
            print("chosen squares")    
            print(square)
            print("\ntheir fitnesses")   
            print(cost_list) 
            print("\n***************************************************")   

            #print to file the new fitnesses
            w.write("%d : %f\t%d : %f\n\n" % (repeat + 1, max(cost_list), self.maxOfFitness_index + 1, self.maxOfFitness))
            for i in range(len(cost_list)):
                w.write("chromosome %d :\t%f\n" % (i+1, cost_list[i]))
            w.write("\n\n") 
     
     
            #if there is no change for a while then get out of this unnecessery loop
            if cost_list == previous_cost_list:
               cost_no_change_count += 1
               if cost_no_change_count == self.noChangeInCostNum:
                   print("Looks like there is no improvement.....")
                   break
            else: 
                cost_no_change_count = 0
            previous_cost_list = cost_list[:]
            


            muteChildren = self.mutation(square)
            print(muteChildren)
            muteChildren.pop()
            print("these are your muted children")
            recoChildren = self.Reconciliation(muteChildren)
            recoChildren.pop()
            print(recoChildren)
            print("and these are your reconciliated children")
            
            #square.clear()
            for re in recoChildren:
                square.append(re)

    
        print("last square")    
        print(square)

        w.close()
        #*********************************************************************************** 
          
        
    def generateParents(self): 
        #initialize square with random numbers
        numarr = [i for i in range(1, self.square_size * self.square_size + 1)]
        square = []
        for x in range(self.parent_count):
            random.shuffle(numarr)
            square.append([numarr[x] for x in range(self.square_size * self.square_size)])
            
        return square

    def sumEval(self):
        return (self.square_size*(self.square_size*self.square_size +1))/2

    def cost(self, square):
        col = 0
        row = 0
        diag1 = 0
        diag2 = 0
        costValue = 0
        
        #substract every sum of column, row, and diagonal from the expected sum.
        for i in range(self.square_size):
            for j in range(self.square_size):
                col += square[i*self.square_size + j]
                row += square[j*self.square_size + i]   
            costValue += abs(self.expectedSum - col) + abs(self.expectedSum - row)
            col, row = 0, 0
            diag1 += square[i*self.square_size + i]
            diag2 += square[(self.square_size - i)*i - i]
            
        costValue += abs(diag1 -self.expectedSum) + abs(diag2 - self.expectedSum)
        return 1 / (costValue + 1)
    
    
    def mutation(self, square):
        
        children = []
        indexes = []
        numberofmutations = int( self.population_count * self.mutation_probability )
        children = random.choices(population=square, k = numberofmutations)
        
        #save the left out parents
        notparents = []
        for s in square:
            if s not in children:
                notparents.append(s)
        
        for x in children:
            
            print("square:")
            print(x)
            indexes.clear()
            indexes = random.choices(population=x, k = 2)
            indexes.sort()
            indexes = [i-1 for i in indexes]
            print("indexes:")
            print(indexes)
            
            #____________________________swap mutation________________________________
#            print("\nswap mutation : ")
#            x[indexes[0]], x[indexes[1]] =  x[indexes[1]], x[indexes[0]]
#            
            #___________________________insert mutation_______________________________
#            print("\ninsert mutation : ")
#            x.insert(indexes[0] + 1, x[indexes[1]])
#            del x[indexes[1] + 1]
#            
            #__________________________scramble mutation______________________________
            print("\nscramble mutation : ")
            temp = x[indexes[0] : indexes[1]]
            random.shuffle( temp )
            for i in range(len(temp)):
                x[indexes[0] + i] = temp[i]
            
            #__________________________inversion mutation_____________________________
#            print("\ninversion mutation : ")
#            temp = x[indexes[0] : indexes[1]]
#            temp.reverse()
#            for i in range(len(temp)):
#                x[indexes[0] + i] = temp[i]
            #_________________________________________________________________________   
            
            print("child:")
            print(x)
         
        for n in notparents:
            children.append(n)    
        notparents.clear()
        return children

        
    def Reconciliation(self, square):
        
        #probability
        numberOfReconciliations = int( self.population_count * self.reconciliation_probability )
        parents = random.choices(population=square, k = numberOfReconciliations)
        
        
        previous = parents[0]
        children = []
        child = []
        
        #iterate over pairs of squares in the parents
        for i in [x for x in range(len(parents)) if x%2 == 0]:
           
            #if odd number of population just copy the last parent into a child
           if (i == len(parents) - 1):
                children.append(parents[i])
                continue
           
           for tmp in range(2):  
               #2 times for each pair of parents
               if tmp == 0:
                   current = parents[i+1] 
                   previous = parents[i]
                   tmp = 1
               else:
                   current, previous = previous, current
               
               print(previous)
               print("square1  \n")
               print(current)
               print("square2  \n")    
               
               child = [0 for i in range(self.square_size*self.square_size)]  
               
               
               #________________________________XMP_____________________________________________
#               print("\n\nReconciliation XMP: \n\n")
#                #random indexes
#               indexes = random.choices(population=[i for i in range(self.square_size*self.square_size)], k = 2)
#               indexes.sort()
#               for ind in indexes:
#                   ind -= 1
#               print(indexes)
#               print("indexes \n\n")           
#               #set child elements in random range to first parent elements
#               for i in range(indexes[1]-indexes[0]):
#                   child[i + indexes[0]] = previous[i + indexes[0]]
#                  
#                #pmx algorithm
#                
#               for i in range(indexes[1]-indexes[0]):
#                   if current[i+indexes[0]] not in child:
#                       if child[current.index(previous[i+indexes[0]])] != 0:
#                           child[current.index(previous[current.index(previous[i+indexes[0]])])] = current[i+indexes[0]]
#                       else:
#                           child[current.index(previous[i+indexes[0]])] = current[i+indexes[0]]
#               
          
               #_______________________________CYCLE____________________________________________            
               print("Reconciliation CYCLE: \n")
               currentchoice = previous[0]
               curchoice_index = 0
               i = 0

               while currentchoice != previous[0] or i==0:
                   i=1
                   child[curchoice_index] = currentchoice
                   curchoice_index = previous.index(current[curchoice_index])
                   currentchoice = previous[curchoice_index]         
              
               #________________________________________________________________________________ 
               
               #set the remaining values 
               for i in range(self.square_size*self.square_size):
                    if child[i] == 0:
                        child[i] = current[i]
                        
               print(child)
               print("child ___________________________ \n")
          
               children.append(child) 
               
        return children
   

#function for rank
def rankify_improved(A): 
    # rank list
    R = [0 for i in range(len(A))] 

    T = [(A[i], i) for i in range(len(A))] 

    T.sort(key=lambda x: x[0]) 
    (rank, n, i) = (1, 1, 0) 
    while i < len(A): 
        j = i 
        # Get number of elements with equal rank 
        while j < len(A) - 1 and T[j][0] == T[j + 1][0]: 
            j += 1
        n = j - i + 1
        for j in range(n): 
            idx = T[i+j][1] 
            R[idx] = rank + (n - 1) * 0.5
        rank += n 
        i += n 
    return R

#main      
f = open('input.txt','r')
inp = []
for x in f:
  inp.append(x)
  
we = magicSquare(int(inp[4])*2, int(inp[4]), int(inp[1]), int(inp[0]), float(inp[2]), float(inp[3]))  
#we = magicSquare(6 ,4, 10, 3, 0.8, 0.8)
we.findBestValues()