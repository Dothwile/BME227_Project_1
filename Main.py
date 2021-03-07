'''
Created on Mon Mar 01 2021

@author: Artur Smiehcowski
'''
# %%
#Imports
import numpy as np
import serial
import time
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
    sample_time ~  sequential list of expected time of each sample
    '''
    # Creates "empty" arrays with np.array of given size, then actually empties them
    total_samples = recording_duration * fs
    sample_data = np.empty([total_samples,n_channels])
    sample_data[:] = np.NaN

    #Fill sample_time array with predicted time of each sample step
    sample_time = []
    for sample_n in range(total_samples):
        sample_time.append((sample_n + 1) * (1/fs))
        
    
    return sample_data, sample_time;

def initialize_plot(sample_data, sample_time):
    '''initialize_plot
    Takes 2 data sets (output from initialize_arrays)

    Returns line objects for future plotting
    sample_lines ~ line objects for plotting
    '''
    plt.figure()
    plt.clf()

    plt.title('Arduino Data')
    plt.xlabel('time(s)')
    plt.ylabel('Voltage(mV)')

    plt.xlim([0,sample_time[-1]])
    plt.ylim([0,5])

    sample_lines = plt.plot(sample_time[:], sample_data)
    plt.show()    
    return sample_lines
    

# %% Method Calls and Figure Saving

out_folder = '.'
sd,st = initialize_arrays(2,3,7)
lines = initialize_plot(sd,st)

print(st)

plt.savefig('ArduinoData_'+time.strftime("%Y-%m-%j_%H-%M-%S",time.localtime()))

