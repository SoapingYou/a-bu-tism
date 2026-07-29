import numpy as np
from scipy.optimize import minimize_scalar

TAU = 2 * np.pi

class lipschitzSolver:
    def lipschitzPhasesToLocation1D(self,data: np.ndarray, eps: float=0.001, t_max:float=1e5) -> float:
        # because this is how you sort an array in np of course
        data = data[data[:, 0].argsort()[::-1]]
        self.s_is = data[:,0]
        self.p_is = data[:,1]
        self.phi_js = self.s_is * self.p_is / (2*np.pi)

        L = 2*np.pi*np.mean(1/self.s_is)          # Lipschitz bound on r(t)
        min_step = 0.01

        threshold = 1 - eps

        t = 0
        t_prev = 0
        while t < t_max:
            r_t = self.r(t)
            if r_t >= threshold:
                result = minimize_scalar(self.negative_r, bounds=(t_prev,t), method="bounded")
                return result.x, -result.fun

            # safe jump: how far can we skip before r could possibly cross threshold?
            step = (threshold - r_t) / L
            # safe jump to next slowest wave peak
            next_cycle_peak = np.ceil((t - self.phi_js[0]) / self.s_is[0])
            next_t = self.phi_js[0] + self.s_is[0]*next_cycle_peak
            other_step = next_t-t
            t_prev = t
            # min_step guards against step -> 0 near threshold
            t = t + np.max([other_step,step, min_step])   

    def r(self,t):
        theta_j_t = (2*np.pi/self.s_is)*t + self.phi_js
        return np.abs(np.mean(np.exp(1j*(theta_j_t))))
    def negative_r(self,t):
        return -self.r(t)

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
