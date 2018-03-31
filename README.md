# grib2numpy
Simple pipeline to download grib2 data from ECMWF, translate grib2 grid format into numpy arrays and visualize them.


Includes:

* __downloader__ - format, for easy downloading of weather data from ECMWF.

* __parser__ - to translate data into numpy array and pickle them (most optimal action - memory and speed wise)

* __plotter__ - to create plots of data, from grib and pickle, visualize them and parse them into gifs (if in sequence)

