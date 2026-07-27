#import functions
from phaseSolutions import phasesToLocation1D
#import dependencies
import numpy as np
import math 


def phasesToLocation1Dtest(trial_num, optional_inputs=None,
                           PRECISION=0.8, TRY_LIMIT=5,  
                           n=5,low=25,high=100, threshold_pi=0.15,
                           verbose=False):
    '''
    Tests phasesToLocation1D 

     - param trial_num is # of trial nums,      ALWAYS INCLUDE THIS!!!
       either consistent with optional_inputs, 
       or # of random trials to run
    - param optional_inputs is either be None, 
       or a numpy array of shape (trial_num,n,2),
       or a numpy array of shape (n,2) if trial_num is 1
    - 
    - param n is # of modules given
    - param low is the lowest si that can be generated
    - param high is the highest si that can be generated
    - param verbose details correct 
    '''

    #Assign training input to optional input if applicable
    _generateNewInput = False
    if optional_inputs is None:
        _generateNewInput = True
    elif not isinstance(optional_inputs, np.ndarray):
        raise ValueError("Please pass optional_inputs as a numpy array")
    elif optional_inputs.ndim==2 and trial_num==1:
        training_input = optional_inputs[np.newaxis, :] 
    elif optional_inputs.ndim != 3:
        raise ValueError("Please pass optional_inputs in shape (trial_num,n,2) or (n,2) if trial_num=1")
    elif optional_inputs.shape[0] != trial_num:
        raise ValueError("Please pass optional_inputs in shape (trial_num,n,2) or (n,2) if trial_num=1")
    else:
        training_input = optional_inputs

    #Create training input 
    if(_generateNewInput):
        rng = np.random.default_rng(seed=42)
        training_input = np.zeros((trial_num,n,2))
        for i in range(trial_num):
            _si = rng.choice(np.arange(low,high),size=n, replace=False)
            _pi = rng.random(size=5) * 2 * np.pi
            training_input[i,:,0] = _si
            training_input[i,:,1] = _pi
    print(training_input[0])    
    #Test training input
    for i in range(trial_num):
        solution = phasesToLocation1D(data=training_input[i], 
                           PRECISION=PRECISION, 
                           TRY_LIMIT=TRY_LIMIT)
        #check if solution works
        for j in range(n):
            si = training_input[i][j][0]
            pi = training_input[i][j][1]
            simulated_pi = (solution%si)*2*np.pi/si
            if np.abs(simulated_pi-pi) > threshold_pi:
                answer = (
                    f"not working in case {i} bc solution {solution} "
                    f"is not consistent with {j}th module:"
                    f" si = {si}  pi = {pi}"
                )
                return answer
            answer = (
                f"works in case {i} solution {solution} is consistent w {j}th module:"
                f"si = {si}  pi = {pi}"
            )
            if(verbose):
                print(answer)
        print(f"solution for case {i} is good")
        return "Works!"


#print(phasesToLocation1Dtest(data, trial_num=1, PRECISION=0.5, TRY_LIMIT=100, n=5, verbose=True))
print(phasesToLocation1Dtest(trial_num=100, PRECISION=0.2, TRY_LIMIT=1000, verbose=True))