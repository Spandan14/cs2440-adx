import numpy as np

# load data from npys
avg_qs_tensor = np.load('avg_qs_tensor.npy')
avg_profits_tensor = np.load('avg_profits_tensor.npy')
avg_active_camps_tensor = np.load('avg_active_camps_tensor.npy')
avg_alpha_tensor = np.load('avg_alpha_tensor.npy')

# print
print(avg_qs_tensor.shape)
print(avg_profits_tensor.shape)
print(avg_active_camps_tensor.shape)
print(avg_alpha_tensor.shape)
