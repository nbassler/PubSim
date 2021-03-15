import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

setup = ['HeV79', 'HeHSG', 'C135V79', 'C12V79', 'C135HSG',
         'C12HSG', 'C135T1', 'NeV79', 'NeHSG', 'NeT1']
# sets individual degrees for poly fit for different ions
degfit = {'Ne': 5, 'He': 6, 'C12': 10, 'C135': 9, }
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

    # Fitting 5th grade polynomial to the ion type used
    fit_data = pd.read_excel(
        '/home/fredrik/projects/PubSim/2000_Furusawa/WIP/RangeShiftOpt/' + ion + '.xlsx')
    x = fit_data['Energy']
    y = fit_data['Thickness']
    P = np.polyfit(x, y, degfit[ion])

    # Applyting poly-fit to energies in paper
    setup_data = pd.read_excel(
        '/home/fredrik/projects/PubSim/2000_Furusawa/WIP/RawData/' + s + '.xlsx')
    X = setup_data['MeV/nuc']
    print(len(X))
    XP = np.zeros(len(X))
    for j in list(range(degfit[ion]+1)):
        XP = XP + P[-j - 1] * X ** j

    # Writing to file
    with open('/home/fredrik/projects/PubSim/2000_Furusawa/WIP/RangeShiftOpt/thickness.txt', 'a') as f:
        np.savetxt(f, XP, fmt='%1.6f')
        f.close()
'''
plt.scatter(x, y)
X = np.arange(0, max(x), max(x)/150)

plt.plot(X, X5, color='red')
plt.title(ion)
plt.show()
'''
