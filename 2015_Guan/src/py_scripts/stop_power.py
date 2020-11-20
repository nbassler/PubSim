import os
import numpy as np

'''
Creates a new stopping power table by weighing all the ones listed in "files" by atomic weight contribution
'''

rel_path = '../template/'

dirname = os.path.dirname(__file__)
data_path = os.path.join(dirname, rel_path)

files = ['H.txt', 'Li.txt', 'C.txt', 'O.txt', 'Al.txt']
weights_by_number = [0.3777, 0.0004, 0.4430, 0.1787, 0.0011]
atom_weights = [1, 7, 12, 16, 27]

weights = np.multiply(weights_by_number, atom_weights)


# Openfing txt file where the data shall be collected
first = True
for i in range(len(files)):
    with open(data_path + files[i], 'r') as f:
        if first is True:
            data = weights[i] / sum(weights) * np.loadtxt(f, skiprows=8)
            first = False
        else:
            data = data + weights[i] / sum(weights) * np.loadtxt(f, skiprows=8)
        f.close()
np.savetxt(data_path + 'result.txt', data, fmt='%.5e', delimiter=' ',
           header='custom stopping power table, derived by weighing the fraction of all individual elements (by weight)', comments='*')


# function for reading all subfolder names from config file
