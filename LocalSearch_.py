import os
import copy
import time
import datetime
import pandas as pd

os.chdir("~/PB1/")

def obj_fn(myvec):
    s1 = myvec[0]
    s2 = myvec[1]
    s3 = myvec[2]
    s4 = myvec[3]
    s5 = myvec[4]
    s6 = myvec[5]
    s7 = myvec[6]
    s8 = myvec[7]
    s9 = myvec[8]
    z = 8*s1 + 11*s2 + 9*s3 + 12*s4 + 14*s5 + \
        10*s6 + 6*s7 + 7*s8 + 13*s9
    
    return z


def bitcomplement(myvec, i):
    """
    Returns: ith Element complemented binary vector
    """
    myvec[i] = int(not(myvec[i]))
    
    return myvec


def gen_neighbourhood(st):
    """
    Returns: bit-complemented neighbourhood from vector
    """
    N = len(st)
    neighbourhood = []
    for index in range(N):
        st_temp = copy.deepcopy(st)
        neighbour = bitcomplement(st_temp, index)
        neighbourhood.append(neighbour)
        
    return neighbourhood


def is_feasible(vector):
    """
    Returns: True if vector violates the constraint
    """
    lhs = vector[0] + 2*vector[1] + 3*vector[2] + 2*vector[3] + 3*vector[4]\
        + 4*vector[5] + vector[6] + 5*vector[7] + 3*vector[8]
    if(lhs <= 16): result = True
    else: result = False
    
    return result


def evaluate(current_vec):
    """
    Args:
        1. current_obj: scalar value
        2. neighbourhood: list of neighbours
        
    Returns:
        1. best_obj: new or old obj
        2. best_vec: new or old vector
    """
    initial_obj = best_obj = obj_fn(current_vec)
    neighbourhood = gen_neighbourhood(current_vec)
    valid_neighbourhood = []
    printout_valid_neighbourhood = []
    for i in range(len(neighbourhood)):
        if is_feasible(neighbourhood[i]):
            valid_neighbourhood.append(neighbourhood[i])
            printout_valid_neighbourhood.append(obj_fn(neighbourhood[i]))
        if not is_feasible(neighbourhood[i]):
            printout_valid_neighbourhood.append("infeasible")
        
    valid_objs = []
    for i in range(len(valid_neighbourhood)): 
        obj_val = obj_fn(valid_neighbourhood[i])
        valid_objs.append(obj_val)
    
    # if neighbour w/ better obj_fn, current_obj updated, else soln found
    max_valid = max(valid_objs)
    if max_valid > best_obj: 
        best_obj = max_valid
        ind = valid_objs.index(max_valid) # which valid_obj is better
        best_vec = valid_neighbourhood[ind] # which vec matches above index
    else: best_vec = current_vec
    
    return (initial_obj, 
            current_vec, 
            best_obj, 
            best_vec, 
            neighbourhood, 
            printout_valid_neighbourhood)
    

def local_search(initial_vec):
    """
    Local search for 9-coefficient knapsack
    """
    ts = [] # iteration
    sts = [] # current vec
    zs = [] # current obj
    neighbourhoods = [] # neighbourhood vecs
    newzs = [] # corres objs
    selections = [] # selected vector
    
    t = 0
    _, _, _, best_vec, _, _ = evaluate(initial_vec)
    while True:
        initial, \
        current_vec, \
        best, \
        best_vec, \
        n_hood, \
        p_v_n_hood = evaluate(best_vec)
        
        sts.append(current_vec)
        zs.append(initial)
        neighbourhoods.append(n_hood)
        newzs.append(p_v_n_hood)
        selections.append(best_vec)
        if initial >= best: 
            print("Initial: {init}".format(init=initial_vec))
            print("After {number} iterations:".format(number=t + 1))
            print("Objective function: {obj}\nSolution: {vec}\n"\
                  .format(obj=best,
                          vec=best_vec))
            ts = [*range(t + 1)]
            record_df = pd.DataFrame.from_dict({
                "t": ts, 
                "St": sts, 
                "z": zs, 
                "Neighbourhood": neighbourhoods, 
                "New z": newzs, 
                "Selected": selections
                })
            now = datetime.datetime.now().strftime("%d-%m-%Y-%H%M%S")
            time.sleep(1)
            # save dataframe to working dir for inspection
            record_df.to_csv("{time}.csv".format(time=now))
            break
        
        t += 1
        
        
if __name__ == "__main__":
    local_search([0, 1, 1, 1, 0, 0, 1, 1, 1])
    local_search([0, 1, 0, 1, 0, 0, 0, 1, 0])
    
