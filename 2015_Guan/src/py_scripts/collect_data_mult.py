import os
import json

rel_path = '../../data/output/'
thickn_char = 76
row_in_detect = 21
header = 'PMMA AvgEnergyPrim DLET DLETPrim DLETProt TLET TLETPrim TLETProt dZ2Beta2 dZ2Beta2Prim dZ2Beta2Prot dZeff2Beta2 dZeff2Beta2Prim dZeff2Beta2Prot tZeff2Beta2 tZeff2Beta2Prim tZeff2Beta2Prot'
dirname = os.path.dirname(__file__)
data_path = os.path.join(dirname, rel_path + 'wdir/')

# This generates a list of all subfolder paths
subfolders = [x[0] for x in os.walk(data_path)][1:]


# Openfing txt file where the data shall be collected
with open(data_path + '../collected_data.txt', 'w') as col:
    col.write(header + '\n')
    # going through subfolders, first writing the LET value as reference (taken from the folder name), then adding the data in the SH-file
    for i in subfolders:
        _, _, filenames = next(os.walk(i))
        for j in filenames:
            if j[0:4] == 'data':
                with open(i + '/' + j, 'r') as f:
                    col.write(i[len(data_path):])
                    col.write(f.readlines()[row_in_detect])
                    f.close()
    col.close()
