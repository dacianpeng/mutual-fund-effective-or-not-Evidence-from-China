import numpy as np

def yearly_return(monthly_α):
    return str((((monthly_α + 1) ** 12 - 1) * 100).round(2)) + '%'

def float_to_percent(float : np.float64):
    return str((float * 100).round(3)) + '%'