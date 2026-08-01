# %%
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize

Array = np.ndarray

# %%
# s_is = 25 * 1.65 ** np.arange(10)
# real_p_i = np.array([6.0, 0.0, 5.15, 0.65, 4.2, 2.55, 1.55, 0.95, 0.55, 0.35]) # x = 123.8
# p_is = np.round(real_p_i * 20) / 20

# %%
def _computeCosine(s: float, p: float, x: float) -> float:
    return np.cos(2 * np.pi / s * x - p)


def errorAtX(x: float, s_is: Array, p_is: Array) -> float:
    cosines_at_x = np.array(
        [_computeCosine(s, p, x) for s, p in zip(s_is, p_is)]
    )
    error_at_x = np.abs(cosines_at_x - 1)
    return np.sum(error_at_x)

def sweepError(s_is: Array, p_is: Array, start=0, stop=22_000, step=2) -> np.ndarray:
    x = np.arange(start, stop, step)
    cosines = np.array(
        [np.cos(2 * np.pi / s * x - p) for s, p in zip(s_is, p_is)]
    )
    error = np.abs(cosines - 1)
    return np.sum(error, axis=0)

def findMinsIdxs(error: np.ndarray, thresh=2) -> np.ndarray:
    lows = np.concat(([False], error < thresh, [False])) # pad with Falses
    transitions = np.diff(lows.astype(np.int8))
    starts, stops = np.where(transitions == 1)[0], np.where(transitions == -1)[0]
    return np.column_stack((starts, stops))

def runOptimize(mins_idxs: np.ndarray, s_is: Array, p_is: Array, step_size=2) -> float:
    mins_x_ranges = mins_idxs * step_size
    for (start, stop) in mins_x_ranges:
        opt = minimize(
            lambda x: errorAtX(x, s_is, p_is),
            (start + stop) / 2,
            bounds=[(start, stop)],
        )

        if opt.fun < 0.1:
            return float(opt.x[0])
    return -1

def phasesToLocation1DOptimize(data: np.ndarray) -> float:
    coarse_sweep = sweepError(data[:, 0], data[:, 1])
    mins = findMinsIdxs(coarse_sweep)
    return runOptimize(mins, data[:, 0], data[:, 1])

def test():
    import math
    TAU = np.pi * 2
    for _ in range(500):
        x = np.random.random() * 2_000 # [0, 500)
        s_is = 25 * 1.65 ** np.arange(10)


        n = np.floor(x / s_is)
        p_is = TAU * x / s_is - TAU * n
        rounded_p_i = np.round(p_is * 20) / 20

        data = np.zeros((10,2))
        data[:, 0] = s_is # 1st col
        data[:, 1] = rounded_p_i # 2nd col

        x_guess = phasesToLocation1DOptimize(data)
        if math.isclose(x, x_guess, rel_tol=25/20):
            print('😀', end=' ')
        else:
            print(f'\nFAILED: {x=}, {x_guess=}, {data=}')
            break
    print()

if __name__ == '__main__':
    test()


