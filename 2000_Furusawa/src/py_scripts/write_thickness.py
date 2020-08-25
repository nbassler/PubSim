import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

setup = ['HeV79', 'HeHSG', 'C135V79', 'C12V79', 'C135HSG',
         'C12HSG', 'C135T1', 'NeV79', 'NeHSG', 'NeT1']

dirname = os.path.dirname(__file__)
data_path = os.path.join(dirname, '../../data/')
first = True
# Looping over all setup types
for s in setup:

    # Find ion type
    if 'He' in s:
        ion = 'He'
    elif 'Ne' in s:
        ion = 'Ne'
    elif 'C12' in s:
        ion = 'C12'
    elif 'C135' in s:
        ion = 'C135'

    # Fitting cubic splines to the ion type used
    fit_data = pd.read_excel(data_path +
                             'processed/' + ion + '.xlsx')
    x = fit_data['Energy']
    y = fit_data['Thickness']
    f2 = interp1d(x, y, kind='cubic')

    # Applyting splines to energies in paper
    setup_data = pd.read_excel(data_path +
                               'raw/' + s + '.xlsx')
    X = setup_data['MeV/nuc']
    print(len(X))
    XP = f2(X)

    # Writing to file
    if first is True:
        first = False
        with open(data_path + 'output/thickness.txt', 'w') as f:
            np.savetxt(f, XP, fmt='%1.6f')
            f.close()
    else:
        with open(data_path + 'output/thickness.txt', 'a') as f:
            np.savetxt(f, XP, fmt='%1.6f')
            f.close()

    plt.scatter(x, y)
    X = np.arange(min(x), max(x), max(x)/150)

    plt.plot(X, f2(X), color='red')
    plt.xlabel('LET')
    plt.ylabel('Range Shifter Thickness [cm]')
    plt.title(ion)
    plt.show()
