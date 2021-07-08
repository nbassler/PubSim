import os
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

'''
Generates a dataframe with the calculated quantities at the specific PMMA depths used
PMMA depths in turn are calculated from dLET_prim
'''
LETs = [[0.9, 1.2, 1.6, 1.8, 1.9, 2.3, 3.0, 5.1, 10.8, 15.2, 17.7, 19.0], [
    1.0, 2.5, 4.3, 6.1, 7.2, 9.6, 12.1, 13.6, 15.2, 16.5, 18.1, 19.5], [2.6, 4.7, 7.3, 11.1, 13.7, 15.4, 16.9, 18.3, 20.2, 21.4]]
file_names = ['summary_all_ions.csv', 'summary_all_ions.csv', 'summary_all_ions.csv']
papers = ['Guan_2015', 'Patel_2017', 'Bronk_2020']
ion = "H"

LETs = [[20.2, 39.8, 63.1, 70.6, 84.3, 100.8, 126.3, 157.6, 196.4, 242.9, 285.8, 308.4]]
file_names = ['summary_all_ions.csv']
papers = ['Bronk_2020']
ion = 'C'

LETs = [[6.6, 11.1, 14.3, 21.9, 33.8, 41.6, 50.4, 57.9, 65.2, 70.3, 73.4]]
file_names = ['summary_all_ions.csv']
papers = ['Bronk_2020']
ion = 'He'

rel_path = '../../data/'
dirname = os.path.dirname(__file__)

# data path should point to the csv-file containing the mean and stderr values for each PMMA thickness
data_path = os.path.join(dirname, rel_path)

for k in range(len(file_names)):
    # loading data into pandas
    with open(data_path + file_names[k], 'r') as col:
        df = pd.read_csv(col, delimiter=',')
    '''
    df.columns = ['stat_moment', 'ion', 'PMMA', 'AvgEnergyPrim', 'Dose', 'DosePrim', 'DoseProt', 'DLET', 'DLETPrim', 'DLETProt', 'TLET', 'TLETPrim', 'TLETProt',
                  'dQ', 'dQPrim', 'dQProt', 'tQ', 'tQPrim', 'tQProt', 'dZeff2Beta2', 'dZeff2Beta2Prim', 'dZeff2Beta2Prot', 'tZeff2Beta2', 'tZeff2Beta2Prim', 'tZeff2Beta2Prot']
    df.columns = ['stat_moment', 'ion', 'PMMA', 'AvgEnergyPrim', 'Dose', 'DosePrim', 'DoseProt', 'DLET', 'DLETPrim', 'DLETProt', 'TLET', 'TLETPrim', 'TLETProt',
                  'dQ_300keV', 'dQPrim_300keV', 'dQProt_300keV', 'tQ_300keV', 'tQPrim_300keV', 'tQProt_300keV', 'dZeff2Beta2_100keV', 'dZeff2Beta2Prim_100keV', 'dZeff2Beta2Prot_100keV', 'tZeff2Beta2_100keV', 'tZeff2Beta2Prim_100keV', 'tZeff2Beta2Prot_100keV']
    '''
    df.columns = ['stat_moment', 'ion', 'PMMA', 'AvgEnergyPrim', 'Dose', 'DosePrim', 'DLET', 'DLETPrim', 'TLET', 'TLETPrim',
                  'dQ_100keV', 'dQPrim_100keV', 'tQ_100keV', 'tQPrim_100keV', 'dZeff2Beta2', 'dZeff2Beta2Prim', 'tZeff2Beta2', 'tZeff2Beta2Prim']

    # splitting mean and stdom
    df_mean = df[df['stat_moment'] == 'mean']
    df_stdom = df[df['stat_moment'] == 'stderr']

    # filtering by ion
    df_mean_ion = df_mean[df_mean['ion'] == ion]
    df_stdom_ion = df_stdom[df_stdom['ion'] == ion]

    thick = df_mean_ion['PMMA'].values
    headers = list(df.columns.values)
    '''
    # creating two new dataframes:One with mean values and one with stds
    for i in thick:
        filt = df['PMMA'] == i
        df_i = df[filt]

        # mean value
        df_mean.loc[str(i)] = df_i.mean()

        # stdom, dividing std with sqrt of number of data-files
        df_stdom.loc[str(i)] = df_i.std().div(math.sqrt(len(df_i.index)))

    df_mean = df_mean.sort_index()
    df_stdom = df_stdom.sort_index()
    thick.sort()
    '''

# First get a cubib interpolationg function for each quantity. This will be held in a dict
# with the key being the header in df_mean and value being the function
    quant_names = list(df_mean_ion.columns[2:])
    splines = {}
    for i in quant_names:
        f2 = interp1d(thick, df_mean_ion[i], kind='cubic')
        splines[i] = f2

    # Check dLET_prim splines to get which PMMA thicknesses will be used for checking all quantities
    x = np.arange(min(thick), max(thick), (max(thick) - min(thick))/10000)
    used_thick = [None] * len(LETs[k])
    for i in range(len(LETs[k])):
        run = 0
        while splines['DLETPrim'](x[run]) < LETs[k][i] * 10:
            run += 1
        used_thick[i] = (x[run] + x[run-1])/2

    # Finally create a dataframe with all interpolated values for the quantities
    quants = [[] for _ in range(len(LETs[k]) + 1)]
    quants[0] = quant_names
    for i in range(len(LETs[k])):
        dat = [None] * len(quant_names)
        for j in range(len(quant_names)):
            dat[j] = np.asscalar(splines[quant_names[j]](used_thick[i]))
        quants[i+1] = dat

    if k == 0:
        df_quants = pd.DataFrame(quants[1:], columns=quants[0])
    else:
        df_quants = df_quants.append(pd.DataFrame(quants[1:], columns=quants[0]))


# Adding paper info to df
pap_data = []
for i in range(len(LETs)):
    for j in range(len(LETs[i])):
        pap_data.append(papers[i])
df_quants['paper'] = pap_data

df_quants.to_csv('test.csv')
