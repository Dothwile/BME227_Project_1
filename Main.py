'''
Created on Mon Mar 01 2021

@author: Artur Smiehcowski
'''
# %%
#Imports
import numpy as np
import serial
import time
import argparse
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
    # Creates zeroed arrays with np.array of given size, then actually empties them
    total_samples = round((recording_duration * fs)+0.5)
    sample_data = np.zeros([total_samples,n_channels])
    sample_data[:] = np.NaN

    #Fill sample_time array with predicted time of each sample step in milliseconds
    sample_time = []
    for sample_n in range(total_samples):
        sample_time.append((sample_n) * (1/fs) * 1000)
        
    
    return sample_data, sample_time;

def initialize_plot(sample_data, sample_time):
    '''initialize_plot
    Takes 2 data sets (output from initialize_arrays)

    Returns line objects for future plotting
    sample_lines ~ line objects for plotting
    '''
    plt.clf()

    plt.title('Arduino Data')
    plt.xlabel('time(s)')
    plt.ylabel('Voltage(V)')

    plt.xlim([0,sample_time[-1]])
    plt.ylim([0,5])

    # Create a list of line objects, 1 per channe
    sample_lines = plt.plot(sample_time[:],sample_data[:],'-')
    
    return sample_lines
    
# %% Input Variable //Will use to set from cmd when implemented, that's just housekeeping
sample_dura = 2
channel_count = 3
sample_freq = 500

# %% Method Calls

fig = plt.figure()
sd,st = initialize_arrays(sample_dura,channel_count,sample_freq)
lines = initialize_plot(sd,st)

# %% Read Serial Data into Array

# Variables and debug prints
port_ID = 'COM3'
sample_count = sd.shape[0]
print(np.shape(sd))
print(sample_count)

fig.show()
with serial.Serial(port=port_ID,baudrate=500000) as arduino_data:

    arduino_data.flushInput() # Flushing at start leads to full line reads unlike in loop

    for sample_index in range(sample_count):
        # Extract data string to parse
        data_string = arduino_data.readline()
        # Split into list of strings
        data_string = data_string.split()
        
        #print(sample_index)
        print(len(data_string))
        #print(sd[sample_index-1,0]) # Values updating properly, nans in places where data_string not full
        print(st[sample_index]) # Time as predicted
        print('Seperator')
        print(st[sample_index-1]) # Time is updating properly


        
        # Uses short circuit logic and to avoid indexing errors when read line empty or short
        if(len(data_string) >= (channel_count + 1) and (st[sample_index] <= int(data_string[0]))):
            st[sample_index] = int(data_string[0])
        

            # Writes the output of each channel to associate column of data array
            # Converts to V
            for channel in range(channel_count):
                sd[sample_index, channel] = int(data_string[channel])*5.0/1024

                # Update the lines
                lines[channel].set_xdata(st[0:sample_index+1])
                lines[channel].set_ydata(sd[0:sample_index+1, channel])
                #print(np.shape(sd))
                plt.pause(0.0001)
            

            sd[sample_index, 0] = int(data_string[1])*5.0/1024

# Close the port
arduino_data.close()

#print(len(st))
#print(st)
#print(sd)

# Figure Saving
out_folder = '.'
plt.savefig(out_folder + '\ArduinoData_'+time.strftime("%Y-%m-%d_%H-%M-%S",time.localtime()))
np.save(out_folder + '\ArduinoData_'+time.strftime("%Y-%m-%d_%H-%M-%S",time.localtime()),sd)
np.save(out_folder + '\ArduinoTime_'+time.strftime("%Y-%m-%d_%H-%M-%S",time.localtime()),st)

