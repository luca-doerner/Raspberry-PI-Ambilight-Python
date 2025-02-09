import numpy as np

# List of tuples (x, y, z)
tuples = [(1, 2, 3), (4, 5, 6), (7, 8, 9)]

# Convert the list of tuples to a NumPy array
arr = np.array(tuples)

# Calculate the mean for each column (x, y, z)
mean_tuple = np.mean(tuples, axis=0)

print(mean_tuple)