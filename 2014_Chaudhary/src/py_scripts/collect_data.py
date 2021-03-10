import os

rel_path = '../../data/output/'
thickn_char = 76
row_in_detect = 8
header = 'PMMA AvgEnergyPrim DLET DLETPrim'
dirname = os.path.dirname(__file__)
data_path = os.path.join(dirname, rel_path + 'wdir/')

# This generates a list of all subfolder paths
subfolders = [x[0] for x in os.walk(data_path)][1:]

# Openfing txt file where the data shall be collected
with open(data_path + '../collected_data.txt', 'w') as col:
    col.write(header + '\n')
    # going through subfolders, first writing the LET value as reference (taken from the folder name), then adding the data in the SH-file
    for i in subfolders:
        with open(i + '/data.txt', 'r') as f:
            col.write(i[thickn_char:])
            col.write(f.readlines()[row_in_detect])
            f.close()
    col.close()

# function for reading all subfolder names from config file
