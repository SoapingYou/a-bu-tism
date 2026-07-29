#import functions
from phases_to_location import phasesToLocation1D, phasesToLocation1DTry2
#import dependencies
import math

import numpy as np

from phases_to_location import phasesToLocation1D


def altPhasesToLocation1Dtest(trials = 10, precision=0.01):
    TAU = np.pi * 2
    for _ in range(trials):
        x = np.random.random() * 500 # [0, 500)
        s_i = np.random.random(5) * 100 # [0, 100)

        n = np.floor(x / s_i)
        p_i = TAU * x / s_i - TAU * n

        data = np.zeros((5,2))
        data[:, 0] = s_i # 1st col
        data[:, 1] = p_i # 2nd col

        x_guess = phasesToLocation1D(data, TRY_LIMIT=10)
        if math.isclose(x, x_guess, rel_tol=precision):
            print('😀', end=' ')
        else:
            print(f'\nFAILED: {x=}, {x_guess=}, {data=}')
            return False
    print()
    return True

def roundedPhasesToLocation1Dtest(trials = 10, precision=1.251):
    TAU = np.pi * 2
    for _ in range(trials):
        x = np.random.random() * 500 # [0, 500)
        s_i = 25 * 1.65 ** np.arange(10)


        n = np.floor(x / s_i)
        p_i = TAU * x / s_i - TAU * n
        rounded_p_i = np.round(p_i * 20) / 20

        data = np.zeros((10,2))
        data[:, 0] = s_i # 1st col
        data[:, 1] = rounded_p_i # 2nd col

        x_guess = phasesToLocation1DTry2(data)
        if math.isclose(x, x_guess, rel_tol=precision):
            print('😀', end=' ')
        else:
            print(f'\nFAILED: {x=}, {x_guess=}, {data=}')
            return False
    print()
    return True


if __name__ == '__main__':
    assert roundedPhasesToLocation1Dtest(500)