#import functions

#import dependencies
import numpy as np
import math 


def phasesToLocation1Dtest(optional_inputs=None, trial_num = 100,
                           PRECISION=0.8, TRY_LIMIT=5,  
                           n=5,low=25,high=100):
    '''
    Tests phasesToLocation1D 

    - param optional_inputs is either be None, 
       or a numpy array of shape (trial_num,n,2),
       or a numpy array of shape (n,2) if trial_num is 1
    - param trial_num is # of trial nums, 
       either consistent with optional_inputs, 
       or # of random trials to run
    - param n is # of modules given
    - param low is the lowest si that can be generated
    - param high is the highest si that can be generated
    '''
    _generateNewInput = False
    if optional_inputs == None:
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

    if(_generateNewInput):
        rng = np.random.default_rng(seed=42)
        test_inputs = np.zeros((trial_num,n,2))
        for i in range(trial_num):
            _si = rng.integers(low,high,size=n)
            _pi = rng.random(size=5) * 2 * np.pi
            training_input[i,:,0] = _si
            training_input[i,:,1] = _pi

    
    for i in range(trial_num):
        solution = phasesToLocation1D(data=training_input[i], 
                           PRECISION=PRECISION, 
                           TRY_LIMIT=TRY_LIMIT)
        #check if solution works
        for j in range(n):
            if not math.isclose(solution%training_input[i][j][0], training_input[i][j][1]):
                answer = (
                    f"not working in case {i} bc solution {solution} "
                    f"is not consistent with {j}th module:"
                    f" si = {training_input[i][j][0]}  pi = {training_input[i][j][1]}"
                )
                return answer
        return "Works!"
            
