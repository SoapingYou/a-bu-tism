import numpy as np


def phasesToLocation1D(data: np.ndarray, PRECISION=0.8, TRY_LIMIT=5) -> float:
    '''
    Convert phase data to a location in the 1D environment
   
    :param nparray data: nx2 np array, with wavelengths (s_i) in 1st col and phases (p_i) in 2nd col
    :param float PRECISION: function will return when error in every module is less than this
    :param int TRY_LIMIT: int, function will only attempt this many iterations before returning


    :return float: -1 on failure, location otherwise
    '''
    s1: float = data[0][0]
    p1: float = data[0][1]
    tries = [(n + p1/(2*np.pi)) * s1 for n in range(TRY_LIMIT)]


    for x in tries:
        try_ = np.array([np.cos(2 * np.pi/s * x - p) for s, p in data])
        error = np.abs(try_ - 1)
        if np.all(error < PRECISION):
            return x


    return -1


if __name__ == '__main__':
    data = np.array([
        [11, 0.56],
        [7, 1.8],
        [5, 3.77],
        [3, 4.18],
        [2, 3.1415],
    ])
    print(f'{phasesToLocation1D(data):.2f}')