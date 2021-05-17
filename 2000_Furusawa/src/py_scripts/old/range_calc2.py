import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

ion = 'He'
df = pd.read_excel('/home/fredrik/projects/PubSim/2000_Furusawa/WIP/RangeShiftOpt/' + ion + '.xlsx')

x = df['Energy']
# print(df)
y = df['Thickness']


X = np.arange(0, max(x), max(x)/150)


pols = 10
P = [[] for _ in range(pols)]
XP = [[0] for _ in range(pols)]
res = np.zeros(pols)

# Produces "pols" sets of Polynomial coefficients P and plotting data XP
for i in list(range(pols)):
    P[i] = np.polyfit(x, y, i, full=True)
    res[i] = P[i][1][0]
#    print(str(i) + ' degree fit: ' + str(P[i][1][0]))

    for j in list(range(i+1)):
        print(i)
        XP[i] = XP[i] + P[i][0][-j - 1] * X ** j

#plt.scatter(list(range(pols)), np.log(res))

plt.scatter(x, y)
plt.plot(X, XP[4], color='orange')
plt.plot(X, XP[7], color='teal')

plt.xlabel('Energy/nucleon [MEV/n]')
plt.ylabel('Range shifter thickness [cm]')
plt.title(ion)


f2 = interp1d(x, y, kind='cubic')
plt.plot(x, f2(x), color='blue')

plt.show()
