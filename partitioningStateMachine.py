import numpy as np
import pandas as pd
## Methods

def index_of_element_in_other_sets(element, array, index):
    for i, s in enumerate(array):
        if element in s:
            return i
    return None

def find_non_similar_lists(list_of_lists):
    non_similar_indexes = []
    similar_elements = {}
    
    for i, sublist in enumerate(list_of_lists):
        similar = False
        for j, other_sublist in enumerate(list_of_lists):
            if i != j and sublist == other_sublist:
                similar = True
                break
        if not similar:
            non_similar_indexes.append(i)
        else:
            if tuple(sublist) not in similar_elements:
                similar_elements[tuple(sublist)] = [i]
            else:
                similar_elements[tuple(sublist)].append(i)
    
    return non_similar_indexes, similar_elements

def separate_indices(input_set, indices):
    index_set = set()
    non_index_set = set()

    for i, char in enumerate(input_set):
        if i in indices:
            index_set.add(char)
        else:
            non_index_set.add(char)
    print(index_set,non_index_set)
    return {frozenset(index_set), frozenset(non_index_set)}

def remove_empty_sets(set_of_sets):
    # Create a copy of the set to avoid modifying the original set during iteration
    set_copy = set_of_sets.copy()
    
    # Iterate over the set copy
    for s in set_copy:
        if not s:  # Check if the frozenset is empty
            set_of_sets.remove(s)  # Remove the empty frozenset from the original set
    
    return set_of_sets

## Initialization
states = "ABCDEFGHIJK"
output = "10"
numberOfVariableStates = 3 ## This variable is used for slicing states
## Table construction
    ## 5 columns ==> [PS, NS_0, NS_1, OUT_0, OUT_1]

## Each PS row value will be state[i] to state[n]. n := states

#stateTable = np.full((numberOfVariableStates, 5), str(np.nan)) ## Row = 5 always

stateTable = pd.read_csv('example.csv', delimiter='\t')
stateTable.index = list(states[:numberOfVariableStates])


stateTable['NS_P_0'] = -1
stateTable['NS_P_1'] = -1
print(stateTable)
print (stateTable)

## Initial Partition
initialPartition = list(stateTable.groupby(['OP_0', 'OP_1'])['PS'].apply(set))

## Only include sets with size >1. Sets with size one can't be separated
## Stop when two consictive itterations are equal ==> In terms of sets


print(initialPartition)

print('\n\n')

## We have to know the state belongs to which partetion

## We can add two new column that is updated each epoch

## After every epoch, group the states by the last column

## The new column tells us the index of the partetion

while (1):
    initialPartition_copy = initialPartition.copy()  # Store a copy for comparison

    for set_ in (initialPartition_copy): ## After finishing this loop, we do partionaning
        print(set_)
        
        for state in set_:
            ## If the element next states belong to the same set, no need for itterating other sets
            if(  (stateTable.loc[state,'NS_0'] in set_) and (stateTable.loc[state,'NS_1'] in set_)):
                print("Inside IF:",set_)
                stateTable.loc[state,"NS_P_0"] = initialPartition.index(set_)
                stateTable.loc[state,"NS_P_1"] = initialPartition.index(set_)
                continue
            stateTable.loc[state,"NS_P_0"] = index_of_element_in_other_sets(stateTable.loc[state,'NS_0'],initialPartition,initialPartition.index(set_))
            stateTable.loc[state,"NS_P_1"] = index_of_element_in_other_sets(stateTable.loc[state,'NS_1'],initialPartition,initialPartition.index(set_))
            print(stateTable)

        for set_2 in initialPartition_copy:
            if (len(set_2)==1): ## No separation for partions with one state
                continue
            garbageList = []
            for state_2 in set_2:
                garbageList.append( [stateTable.loc[state_2,"NS_P_0"],stateTable.loc[state_2,"NS_P_1"]] )
            print("Garbage list",garbageList)

            non_similar_indexes, similar_elements = find_non_similar_lists(garbageList)

            print(non_similar_indexes)
            print(similar_elements)
            print('\n')
            if not (len(non_similar_indexes)==0):
                for i,state_2 in enumerate(set_2.copy()):
                    print(i,state_2)
                    if (i==non_similar_indexes[i]): ## The index i indicates the element which needs part
                        initialPartition.append(set(state_2))
                        set_2.remove(state_2)
            print("Here!",len(similar_elements.values()))
            #if not (len(similar_elements)==0):
             #   for elements, indexes in similar_elements.items():
              #      print(f"{elements}: {indexes}")
               #     break
            for i in similar_elements.keys(): ## The i is SOMETHING ...
                print(i)
                for similar_indecies in similar_elements.values():
                    print(similar_indecies) ## Now seprate set from function according to j
                    print("Last Line",remove_empty_sets(separate_indices(set_2,similar_indecies)))
                    initialPartition.append(remove_empty_sets(separate_indices(set_2,similar_indecies)))
                    print(set_2)
                    initialPartition.remove(set_2)
                    break
            print(initialPartition)
            break

    ## initialPartition.remove(set_2) Do this
    break