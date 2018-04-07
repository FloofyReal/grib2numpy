# DEPRECEATED - SHOULD NOT USE

from os import walk
import pygrib
import numpy as np
import cPickle as pickle

source_path = '/home/floofy/DP/data/ECMWF/'
end_path = '/home/floofy/DP/data/ECMWF/PARSED/'
filename1 = '131x151'
filename2 = '64x64'
filename3 = '32x32'
params = ['Temperature']
params_more1 = ['Specific humidity', 'Cloud cover']
params_more2 = ['Geopotential', 'Logarithm of surface pressure']
params_more3 = ['U component of wind', 'V component of wind']


def grb_to_grid(grb_obj):
    n_levels = len(grb_obj)
    levels = np.array([grb_element['level'] for grb_element in grb_obj])
    indexes = np.argsort(levels)[::-1] # highest first
    cube = np.zeros([n_levels, grb_obj[0].values.shape[0], grb_obj[0].values.shape[1]], dtype=np.float32)
    # cube = np.zeros([n_levels, grb_obj[0].values.shape[0], grb_obj[0].values.shape[1]]) # default float64
    for i in range(n_levels):
            cube[i,:,:] = grb_obj[indexes[i]].values
            cube_dict = {'data' : cube, 'units' : grb_obj[0]['units'],
                         'levels' : levels[indexes]}
    return cube, cube_dict

def get_all_files(source_path, filename):
    fullpath = source_path + filename
    f = []
    for (dirpath, dirnames, filenames) in walk(fullpath):
        f.extend(filenames)
        break
    return f

# should be in main? nah.
filename = filename2

file_names = get_all_files(source_path=source_path, filename=filename)
file_names.sort()

full_filepaths = []
for file_name in file_names:
    full_filepaths.append(source_path + filename + '/' + file_name)

data = []
for f in full_filepaths:
    print f
    mf = pygrib.open(f)
    for p in params:
        try:
            grb = mf.select(name=p)

            print 'From: ' + str(grb[0]['date']) + '.. To: ' + str(grb[-1]['date'])
        except:
            continue
        month, _ = grb_to_grid(grb)
        print len(month)/24
        for hour in month:
            data.append(hour)

name = end_path + filename + '/' + p + '.pkl'
print(name)
with open(name, 'wb') as f:
    pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
