import numpy as np

def yearly_return(result):
    return str((((result.params[0] + 1) ** 12 - 1) * 100).round(2)) + '%'

def float_to_percent(float : np.float64):
    return str((float * 100).round(3)) + '%'