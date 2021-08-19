import os
import copy
import time
import datetime
import pandas as pd

os.chdir("~/PB1/")

def obj_fn(myvec):
    """ Computes objective function value for a given coefficient vector.
    Args:
        myvec (list): Binary vector of coefficients.
    Returns:
        z (int): Objective function value.
    """
    s1 = myvec[0]
    s2 = myvec[1]
    s3 = myvec[2]
    s4 = myvec[3]
    s5 = myvec[4]
    s6 = myvec[5]
    s7 = myvec[6]
    s8 = myvec[7]
    s9 = myvec[8]
    # define objective function below
    z = 8*s1 + 11*s2 + 9*s3 + 12*s4 + 14*s5 + \
        10*s6 + 6*s7 + 7*s8 + 13*s9
    
    return z


def bitcomplement(myvec, i):
    """ Performs a single-bit complement of vector at ith position.
    Args:
        myvec (list): Vector to be complemented.
        i (int): Position in vector to be complemented.
    Returns:
        myvec (list): ith Element complemented binary vector.
    """
    myvec[i] = int(not(myvec[i]))
    
    return myvec


def gen_neighbourhood(st):
    """ Generates neighbourhood of bit complemented vectors based on st.
    Args:
        st (list): Vector on which neighbourhood generation is based.
    Returns:
        neighbourhood (list): Bit complemented neighbours of input vector.
    """
    N = len(st)
    neighbourhood = []
    for index in range(N):
        st_temp = copy.deepcopy(st) # avoid modifying st, new value in memory
        neighbour = bitcomplement(st_temp, index)
        neighbourhood.append(neighbour)
        
    return neighbourhood


def is_feasible(vector):
    """ Checks whether vector violates given knapsackk problem constraint.
    Args:
        vector (list): Vector for evaluation.
    Returns:
        True (boolean) [doesn't violate] if LHS <= 16 else False (boolean).
    """
    lhs = vector[0] + 2*vector[1] + 3*vector[2] + 2*vector[3] + 3*vector[4]\
        + 4*vector[5] + vector[6] + 5*vector[7] + 3*vector[8]
    if(lhs <= 16): result = True
    else: result = False
    
    return result


def evaluate(current_vec):
    """ Vector evaluate and update procedure.
    Args: 
        current_vec (list): Best vector so far.
    Returns:
        initial_obj (int): Initial (current) vector scalar objective function value. 
        current_vec (list): Initial (current) vector.
        best_obj (int): Updated scalar objective function value.
        best_vec (list): Updated vector depending on obj value.
        neighbourhood (list): List of generated neighbours.
        printout_valid_neighbourhood (list): Valid neighbours also indicating 
        infeasible solutions.
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
    """ Local search for 9-coefficient knapsack.
    Args:
        initial_vec (list): Initial vector for search procedure.
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
        
        # store values for printouts
        sts.append(current_vec) # add current vector
        zs.append(initial) # add initial vector
        neighbourhoods.append(n_hood) # add neighbourhood
        newzs.append(p_v_n_hood) # add valid naighbourhood for printout
        selections.append(best_vec) # add best vector
        
        if initial >= best: 
            print("Initial: {init}".format(init=initial_vec))
            print("After {number} iterations:".format(number=t + 1))
            print("Objective function: {obj}\nSolution: {vec}\n"\
                  .format(obj=best,
                          vec=best_vec))
            ts = [*range(t + 1)]
            
            # create record_df for printout purposes
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
