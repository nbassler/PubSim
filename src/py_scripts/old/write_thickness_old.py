import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

setup = ['HeV79', 'HeHSG', 'C135V79', 'C12V79', 'C135HSG',
         'C12HSG', 'C135T1', 'NeV79', 'NeHSG', 'NeT1']

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
    P5 = np.polyfit(x, y, 5)

    # Applyting poly-fit to energies in paper
    setup_data = pd.read_excel(
        '/home/fredrik/projects/PubSim/2000_Furusawa/WIP/RawData/' + s + '.xlsx')
    X = setup_data['MeV/nuc']
    X5 = P5[0] * X ** 5 + P5[1] * X ** 4 + P5[2] * X ** 3 + P5[3] * X ** 2 + P5[4] * X + P5[5]

    # Writing to file
    with open('/home/fredrik/projects/PubSim/2000_Furusawa/WIP/RangeShiftOpt/thickness_old.txt', 'a') as f:
        np.savetxt(f, X5, fmt='%1.6f')
        f.close()
'''
plt.scatter(x, y)
X = np.arange(0, max(x), max(x)/150)

plt.plot(X, X5, color='red')
plt.title(ion)
plt.show()
'''
