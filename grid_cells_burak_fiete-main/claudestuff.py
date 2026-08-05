"""
evaluate_grid.py

Standalone script version of the "Integrate random trajectory" section of
evaluate_grid.ipynb (cell 10), wrapped into a reusable function.

It takes a velocity trajectory (input_v), simulates a Burak & Fiete grid
cell network on it, and decodes ("reconstructs") position from the
simulated network activity using the same blob-tracking + linear-rescaling
procedure the notebook uses (analysis.model_prediction).
"""

import numpy as np
import torch

from options import Options
from grid import Grid
import analysis


def simulate_and_decode(input_v, dt=1e-3, n=100, alpha=0.1, lambda_net=17,
                         target_mean_speed=None, device=None, verb=True):
    """Simulate a Burak & Fiete grid-cell network on a velocity trajectory
    and decode position from the resulting activity.

    Parameters
    ----------
    input_v : array-like, shape (seq_len, 2)
        Velocity trajectory to drive the network with, e.g. from
        trajectory_generator.generate_trajectory()['input_v'].squeeze().
        The network was tuned assuming speeds on the order of ~0.8 (its
        units are effectively "meters/second" given box_width=2.2 and
        dt~1e-3-1e-4). If your input_v comes from a different generator
        with a different scale (e.g. values up to 100), don't just divide
        by an arbitrary constant -- pass target_mean_speed instead (see
        below) so it gets rescaled to the range the network expects.
        Feeding in velocities that are too large can saturate/break the
        attractor bump, not just throw off decoding.
    dt : float
        Integration time step, in seconds (e.g. 1e-3).
    n : int
        Grid side length; the network has n**2 neurons.
    alpha : float
        Strength of the velocity input (passed to Options).
    lambda_net : float
        Approximate number of neurons between two blob centers (passed to
        Options).
    target_mean_speed : float or None
        If given, input_v is rescaled (uniformly, preserving direction) so
        that its mean speed (mean of the per-step vector norms) equals
        this value before simulating. Use this instead of manually
        guessing a scale factor -- e.g. if input_v comes from a generator
        with a different unit/range than the notebook's own trajectory
        generator (whose mean speed is ~0.8). If None, input_v is used
        as-is.
    device : str or None
        'cuda' or 'cpu'. Defaults to cuda if available, else cpu.
    verb : bool
        Print progress / decoding diagnostics.

    Returns
    -------
    dict with keys:
        'S'          : simulated network activity, shape (seq_len, n**2)
        'pos'        : true position, shape (seq_len, 2) -- obtained by
                        integrating the (possibly rescaled) input_v,
                        starting from the origin
        'pos_pred'   : decoded (rescaled) position, shape (seq_len-1, 2)
        'prop_factor': estimated scale factor between decoded and true position
        'r2'         : R^2 of the linear fit used to rescale decoded position
        'scale_factor': the factor input_v was multiplied by (1.0 if
                        target_mean_speed was None)
    """
    if device is None:
        device = 'cuda' if torch.cuda.is_available() else 'cpu'

    input_v = np.asarray(input_v, dtype=float)

    scale_factor = 1.0
    if target_mean_speed is not None:
        current_mean_speed = np.linalg.norm(input_v, axis=1).mean()
        if current_mean_speed > 0:
            scale_factor = target_mean_speed / current_mean_speed
        input_v = input_v * scale_factor
        if verb:
            print(f'rescaled input_v by {scale_factor:.4g} '
                  f'(mean speed {current_mean_speed:.4g} -> {target_mean_speed:.4g})')

    options = Options(lambda_net=lambda_net)
    options.dt = dt
    options.n = n
    options.alpha = alpha
    options.device = device

    if verb:
        print('device :', options.device)

    grid = Grid(options)

    # grid.simulate always returns a leading batch dimension (shape
    # (batch, seq_len, n**2)); squeeze it out so decoding operates on
    # (seq_len, n**2) as intended (the notebook's cell 10 skips this,
    # which can make analysis.blob_center's indexing ambiguous and
    # produce NaNs during decoding).
    S = grid.simulate(input_v, silent=not verb, load=False)
    S = S.squeeze(0) if S.dim() == 3 else S

    # True position, obtained by integrating the velocity trajectory
    # itself (starting at the origin) -- this is what decoded position
    # gets rescaled against.
    pos = np.cumsum(input_v, axis=0) * dt

    pos_pred, prop_factor, r2 = analysis.model_prediction(S, pos, verb=verb)

    return {
        'S': S,
        'pos': pos,
        'pos_pred': pos_pred,
        'prop_factor': prop_factor,
        'r2': r2,
        'scale_factor': scale_factor,
    }


# if __name__ == '__main__':
#     # Quick smoke test with a simple hand-built input_v: dt = 0.001,
#     # n=40 (rather than the notebook's default n=100, purely to keep this
#     # smoke test fast on CPU -- n=100 works the same way but is much
#     # slower without a GPU).
#     dt = 1e-3
#     seq_len = 2000
#     rng = np.random.default_rng(0)
#     input_v = 0.5 * rng.standard_normal((seq_len, 2))  # m/s, random walk

#     result = simulate_and_decode(input_v, dt=dt, n=40, verb=True)
#     print('pos_pred shape:', result['pos_pred'].shape)
#     print('prop_factor:', result['prop_factor'], 'r2:', result['r2'])