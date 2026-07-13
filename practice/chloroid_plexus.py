from scipy.io import mmread

# Load directly into a dense numpy array
dense_array = mmread('your_matrix.mtx').toarray()