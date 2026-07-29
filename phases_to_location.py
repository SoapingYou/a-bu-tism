import numpy as np

TAU = 2 * np.pi

def phasesToLocation1D(data: np.ndarray, PRECISION=0.05*2*np.pi, TRY_LIMIT=5) -> float:
    '''
    Convert phase data to a location in the 1D environment
   
    :param nparray data: nx2 np array, with wavelengths (s_i) in 1st col and phases (p_i) in 2nd col
    :param float PRECISION: (radians) how close in phase the real p_i and the simulated p_i_s
    :param int TRY_LIMIT: int, function will only attempt this many iterations before returning


    :return float: -1 on failure, location otherwise
    '''
    # because this is how you sort an array in np of course
    data = data[data[:, 0].argsort()[::-1]]

    s_is = data[:, 0]
    p_is = data[:, 1]
    tries = [(n + p_is[0]/(2*np.pi)) * s_is[0] for n in range(TRY_LIMIT)]


    for x in tries:
        n = np.floor(x / s_is)
        new_p_is = TAU * x / s_is - TAU * n

        error = np.abs(p_is - new_p_is)
        if np.all(error < PRECISION):
            return x


    return -1

def phasesToLocation1DTry2(data: np.ndarray):
    # ! p_i is in radians!
    data = data[data[:, 0].argsort()[::-1]]
    s_is = data[:, 0]
    p_is = data[:, 1]

    for i, p in enumerate(p_is):
        if p > np.pi:
            p_is[i] -= TAU

    best_guess = p_is[0] * s_is[0] / TAU
    for s, p in data[1:]:
        n = np.round(best_guess/s - p/TAU) # blame: Matthew
        best_guess = (TAU * n + p) * s / TAU
    return best_guess

if __name__ == '__main__':
    import matplotlib.pyplot as plt

    # data = np.array([
    #     [11, 0.56],
    #     [7, 1.8],
    #     [5, 3.77],
    #     [3, 4.18],
    #     [2, 3.1415],
    # ])
    data = np.zeros((10,2))
    data[:, 0] = 25 * 1.65 ** np.arange(10)
    real_p_i = np.array([6.0, 0.0, 5.15, 0.65, 4.2, 2.55, 1.55, 0.95, 0.55, 0.35]) # x = 123.8
        
    rounded_p_i = np.round(real_p_i * 20) / 20
    print(rounded_p_i)
    data[:, 1] = rounded_p_i
    # data = np.array([[3., 5.026548245743669], [1., 1.8849555921538759]])


    xaxis = np.arange(0, 30, 0.1)
    for (s, p) in data:
        plt.plot(xaxis, np.cos(2 * np.pi / s * xaxis - p))
    x = phasesToLocation1DTry2(data)
    plt.vlines(x, -1, 1, 'k', 'dashed')
    print(f'{x:.2f}')
    plt.show()
