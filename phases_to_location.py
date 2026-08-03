from typing import Any

import numpy as np
import numba as nb
from numpy import floating

TAU = 2 * np.pi


@nb.njit
def phase_error(guess: float, data: np.ndarray) -> floating[Any]:
    """
    Calculate metric for evaluating best candidate (lower is better).
    :param float guess: guess for position in cm
    :param nparray data: nx2 np array, with wavelengths (s_i) in 1st col and phases (p_i) in 2nd col
    :return float: metric for finding best candidate
    """
    s_is = data[:, 0]
    p_is = data[:, 1]

    predicted = (TAU * guess / s_is) % TAU
    measured = p_is % TAU

    diff = (predicted - measured + np.pi) % TAU - np.pi  # shortest angular distance rad (-pi<diff<pi)
    return np.sum(diff ** 2)


@nb.njit
def greedy(data: np.ndarray, initial_guess: float) -> float:
    """
    Use Alex's greedy algorithm to find the best guess (cm) given rough initial guess.
    :param nparray data: nx2 np array, with wavelengths (s_i) in 1st col and phases (p_i) in 2nd col
    :param float initial_guess: initial rough guess for position in cm
    :return float: best guess based on initial
    """
    guess = initial_guess
    for s, p in data[1:]:
        n = np.round(guess / s - p / TAU)
        guess = (TAU * n + p) * s / TAU
    return guess


def phasesToLocation1DProgressive(data: np.ndarray, prev_x: float):
    """
    Use Alex's algorithm over multiple period candidates to find best guess for location (cm).
    :param float prev_x: previous decoded location, in cm
    :param nparray data: nx2 np array, with wavelengths (s_i) in 1st col and phases (p_i) in 2nd col
    :return float: current decoded location, in cm
    """
    data = data[data[:, 0].argsort()[::-1]].copy()

    for i in range(data.shape[0]):
        if data[i, 1] > np.pi: data[i, 1] -= TAU

    s_0, p_0 = data[0]

    base_guess = p_0 * s_0 / TAU

    # only search around prev position
    k_prev = int(np.floor(prev_x / s_0))
    ks = (k_prev, k_prev + 1)

    best_guess = None
    best_err = np.inf

    for k in ks:
        guess = greedy(data, base_guess + k * s_0)
        err = phase_error(guess, data)

        if err < best_err:
            best_err = err
            best_guess = guess

    return best_guess
