import numpy as np

# Experimental data: [length, turns], time_taken
# Keep adding more data points to improve the model
data = [
    ([60, 20], 4.0),
    ([65, 25], 4.5),
    ([70, 22], 4.7),
    ([75, 30], 5.2),
    ([80, 35], 5.8)
]

def regress():
    A = np.array([[length, turns, 1] for (length, turns), _ in data])  # n x 3
    T = np.array([time for _, time in data])                           # n

    # Solve using least squares
    X = np.linalg.lstsq(A, T, rcond=None)[0] # A.t() * A * X = A.t() * T

    return X


