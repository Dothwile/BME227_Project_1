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

# Create parser to feed into read_and_plot_serial_data method
parser = argparse.ArgumentParser(description='Read, plot, and save multichannel EMG data from a connected device in real time')

# Add arguments and help text
parser.add_argument('com_port',help='Port of connected EMG device',type=str)
parser.add_argument('recording_duration',help='Duration of EMG sampling in seconds',type=float)
parser.add_argument('n_channels',help='How many sample channels of EMG device',type=int)
parser.add_argument('fs',help='Frequency of samples taken from EMG, should match device frequency',type=float)
parser.add_argument('--out_folder',help='Filepath location where figures and data are saved, default to current path',type=str)

# Collect arguments
args = parser.parse_args()

def read_and_plot_serial_data(com_port, recording_duration, n_channels, fs, out_folder='.'):
    '''read_and_plot_serial_data
   Takes 3 numbers and 2 strings
   com_port(str) ~ string ID of COM port devie is connected to
   recording_duration(num) ~ length of data recording in seconds
   n_channels(int) ~ number of data recording channels in EMG device
   fs(num) ~ frequency of EMG recording device
   out_folder(str) ~ filepath that figures and data are saved to, defaults to current location
    ''' 

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
        plt.xlabel('time(ms)')
        plt.ylabel('Voltage(V)')
    
        plt.xlim([0,sample_time[-1]])
        plt.ylim([0,5])
    
        # Create a list of line objects, 1 per channe
        sample_lines = plt.plot(sample_time[:],sample_data[:],'-')
        
        return sample_lines
    
    # %% Method Calls
    
    plt.figure().show()
    sd,st = initialize_arrays(recording_duration,n_channels,fs)
    lines = initialize_plot(sd,st)
    
    # %% Read Serial Data into Array
    
    # Variables and debug prints
    sample_count = sd.shape[0]
    
    with serial.Serial(port=com_port,baudrate=500000) as arduino_data:
    
        #arduino_data.flushInput() # Flushing at start leads to full line reads unlike in loop
    
        for sample_index in range(sample_count):
            # Extract data string to parse
            data_string = arduino_data.readline().decode('ascii')
            # Split into list of strings
            data_string = data_string.split()
            
            # Uses short circuit logic and to avoid indexing errors when read line empty or short
            if(len(data_string) >= (n_channels + 1) and (st[sample_index] >= int(data_string[0]))):
                st[sample_index] = int(data_string[0])
            
                # Writes the output of each channel to associate column of data array
                # Converts to V
                for channel in range(n_channels):
                    sd[sample_index, channel] = int(data_string[channel+1])*5.0/1024
            else: # If data readline is not full, consider it a dropped point and increase time sample index
                st[sample_index] = int(data_string[0])
            
            # Seperate check and loop for plot updates reduces net operations per cycle
            if((sample_index % 50) == 0):
                for channel in range(n_channels):                
                    # Update the lines
                    lines[channel].set_xdata(st[0:sample_index+1])
                    lines[channel].set_ydata(sd[0:sample_index+1, channel])
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
    
# %% Call the whole thing
read_and_plot_serial_data(args.com_port, args.recording_duration, args.n_channels, args.fs, args.out_folder)