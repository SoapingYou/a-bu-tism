import numpy as np

class PhaseFromActivity:
    def __init__(self, activity):
        self.activity = activity

    def get_phase(self):
        return np.argmax(self.activity)