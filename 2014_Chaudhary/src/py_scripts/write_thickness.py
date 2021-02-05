import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d


dirname = os.path.dirname(__file__)
data_path = os.path.join(dirname, '../../data/')

# Fitting cubic splines to the ion type used
fit_data = pd.read_excel(data_path +
                         'processed/' + 'E_and_LET' + '.xlsx')
x = fit_data['DLETPrim']/10
y = fit_data['PMMA']
f2 = interp1d(x, y, kind='cubic')
# Applyting splines to energies in paper
setup_data = pd.read_excel(data_path +
                           'processed/' + 'paper_LET' + '.xlsx')
X = setup_data['DLETPrim']
print(len(X))
XP = f2(X)
# Writing to file
with open(data_path + 'output/thickness.txt', 'w') as f:
    np.savetxt(f, XP, fmt='%1.6f')
    f.close()

plt.scatter(x, y)
X = np.arange(min(x), max(x), max(x)/150)
plt.plot(X, f2(X), color='red')
plt.xlabel('LETd_Primary')
plt.ylabel('Range Shifter Thickness [cm]')
plt.title('ion')
plt.show()
