'''
Created on Mon Mar 01 2021

@author: Artur Smiehcowski
'''
# %%
#Imports
import numpy as np
import serial
from matplotlib import pyplot as plt

# %% Method Definition

def initialize_arrays(recording_duration, n_channels, fs):
    '''initialize_arrays
    Takes 3 numbers (type nonspefic):
    recording_duration ~ duration of EMG recording in seconds
    n_channels ~ number of recording channels
    fs ~ the sampling frequency in Hz

    Returns 2 NumPy arrays
    sample_data ~ array of NANs where rows are samples and columns are channels
    sample_time ~ expected time of each sample
    '''
    # Creates "empty" arrays with np.array of given size, then actually empties them
    sample_data = np.empty([recording_duration * fs,n_channels])
    sample_data[:] = np.NaN
    
    sample_time = np.empty([n_channels, 1])
    sample_time[:] = 1/fs
    
    return sample_data, sample_time;

def initialize_plot(sample_data, sample_time):
    '''initialize_plot
    Takes 2 data sets (output from initialize_arrays)

    Returns line objects for future plotting
    sample_lines ~ line objects for plotting
    '''

    

# %% Method Calls

sd,st = initialize_arrays(2,3,7)
print(st)
initialize_plot(sd,st)
