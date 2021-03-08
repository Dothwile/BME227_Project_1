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
    total_samples = round((recording_duration * fs)+0.5)
    sample_data = np.zeros([total_samples,n_channels])
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
    plt.clf()

    plt.title('Arduino Data')
    plt.xlabel('time(s)')
    plt.ylabel('Voltage(V)')

    plt.xlim([0,sample_time[-1]])
    plt.ylim([0,5])

    # Create a list of line objects, 1 per channe
    sample_lines = plt.plot(sample_time[:],sample_data[:],'-')
    
    return sample_lines
    

# %% Method Calls

fig = plt.figure()
sd,st = initialize_arrays(500,3,250)
lines = initialize_plot(sd,st)

# %% Read Serial Data into Array

port_ID = 'COM5'
sample_count = sd.shape[0]
channel_count = sd.shape[1]
print(channel_count)
print(np.shape(sd))

fig.show()
with serial.Serial(port=port_ID,baudrate=500000) as arduino_data:
    for sample_index in range(sample_count):
        # Extract data string to parse
        data_string = arduino_data.readline()
        # Split into list of strings
        data_string = data_string.split()
        
        # Add time of sample to the time array, converting from millisec to sec
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

        # Update the lines
        #lines[0].set_xdata(st[0:sample_index+1])
        #lines[0].set_ydata(sd[0:sample_index+1, 0])


        #print(sd[0:sample_index+1, 0])
        print(st[sample_index])
        #print(np.shape(sd))
        plt.pause(0.0001)


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

