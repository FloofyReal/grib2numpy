import imageio
from os import walk
 
def saveGIFBatch(directory, path, name=''):
    """
    saves the GIFs in batch to the directory wit the given filename
    """
    # for each frame in batch
    images = []
    for filename in directory:
        print(filename)
        images.append(imageio.imread(filename))

    name_gif = path + '/' + name + '.gif'
    imageio.mimsave(name_gif, images)


def get_all_files(source_path, filename):
    fullpath = source_path + filename
    f = []
    for (dirpath, dirnames, filenames) in walk(fullpath):
        f.extend(filenames)
        break
    return f

# should be in main? nah.
source_path = "C:/Users/Floofy/Tensorflow_win/DP_code/grib2numpy/plotter"
filename = '/gif/teplota0101/'
endfile = '/gif/gifs/'

file_names = get_all_files(source_path=source_path, filename=filename)
file_names.sort()

full_filepaths = []
for file_name in file_names:
    full_filepaths.append(source_path + filename + '/' + file_name)

saveGIFBatch(directory=full_filepaths, path=source_path+endfile, name='teplota_0101')