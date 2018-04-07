from os import walk
import pygrib
import numpy as np
import cPickle as pickle

source_path = '/home/floofy/DP/data/ECMWF/'
end_path = '/home/floofy/DP/data/ECMWF/'
filename1 = '131x151'
filename2 = '64x64'
filename3 = '32x32'
# params = ['Temperature']
params = ['Temperature','Specific humidity', 'Cloud cover']
params_more2 = ['Geopotential', 'Logarithm of surface pressure']
params_more3 = ['U component of wind', 'V component of wind']


def grb_to_grid(grb_obj):
    n_levels = len(grb_obj)
    cube = np.zeros([n_levels, grb_obj[0].values.shape[0], grb_obj[0].values.shape[1]], dtype=np.float32)
    # cube = np.zeros([n_levels, grb_obj[0].values.shape[0], grb_obj[0].values.shape[1]]) # default float64
    time = []
    for i in range(n_levels):
            cube[i,:,:] = grb_obj[i].values

            time_i = grb_obj[i].validDate
            # print(i, time_i.ctime())
            if (i % 24) is not time_i.hour or (i // 24)+1 is not time_i.day:
                print('ERROR - BAD ORDER')
                break
            # print(i % 24, (i // 24)+1)
            # print(time_i.hour, time_i.day)

            time.insert(i, time_i)
    return cube, time

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

for p in params:
    data = []
    print p
    for f in full_filepaths:
        print f
        mf = pygrib.open(f)
        try:
            grb = mf.select(name=p)
            print 'From: ' + str(grb[0]['date']) + '.. To: ' + str(grb[-1]['date'])
        except:
            continue
        month, time = grb_to_grid(grb)
        print len(month)/24
        for hour,hour_t in zip(month, time):
            data.append([hour, hour_t])

    name = end_path + filename + '/' + p + '.pkl'
    print(name)
    with open(name, 'wb') as f:
        pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
