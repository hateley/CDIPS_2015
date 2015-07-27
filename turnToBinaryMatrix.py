import numpy as np

def turnToBinaryMatrix(M):
    nonZero = np.flatnonzero(M)
    np.put(M, nonZero, 1)
    return M
