# grib2numpy
Simple pipeline to translate grib2 grid format into numpy arrays

Includes:

-downloader format, for easy downloading of weather data from ECMWF.
-parser to translate data into numpy array and pickle them (most optimal action - memory and speed wise)
-plotter - to create plots of data, from grib and pickle, visualize them and parse them into gifs (if in sequence)