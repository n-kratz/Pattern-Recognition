
if __name__ == "__main__":
	import sys, time

	import numpy as np
	import matplotlib.pyplot as plt
	import scipy.io as sio
	from datetime import datetime

	def rehab_lab2_function(emg):
		import matplotlib.pyplot as plt
		import numpy as np
		from scipy import signal

		from scipy.fft import fft, fftfreq

		raw_frequency = fft(emg);
		a, b = signal.butter(2, [20, 50], btype='bandpass', fs=200) #we chose a 20-55Hz BPF
		filtered_t = signal.lfilter(a, b, emg)
		filtered_frequency = fft(filtered_t);
		rectified_t = np.abs(filtered_t)

		rectified_t = np.transpose(rectified_t)

		MAV = np.zeros((8, 1));

		for q in range(0, 8):
			for i in range(0, 1):
				MAV[q][i] = np.mean(rectified_t[q][i*100: (i*100)+99], axis=0)

		classifier = np.zeros((8, 1))
		threshold = [10, 8, 15, 10, 15, 10, 12, 15] #these are the thresholds we determined for each electrode

		for q in range(0, 8):
			for i in range(0, 1):
				if MAV[q][i] > threshold[q]:
					classifier[q][i] = 1 #1 is close
				else:
					classifier[q][i] = 0

		close = np.zeros(1)
		temp = np.sum(classifier, 0)
		close = temp >= 4
		return close

	# Import local packages
	sys.path.insert(0,'../')
	from mite.inputs.MyoArmband import MyoArmband

	# Connect to Sense Controller
	print( "Initializing Myo EMG...", flush=True )
	myo = MyoArmband(mac = 'eb:33:40:96:ce:a5' )
	# time.sleep(2)
	myo.run( display = False )
	#myo.view() uncomment to see visualization
	print('Done.', flush=True)

	print('Collecting data...')
	# Collect 10s worth of data 
	run_time = 10
	t0 = time.time() 
	emg_datarest = []
	count = 0

	while time.time() - t0 < run_time:
		emg = myo.state
		if emg is not None:
			emg_datarest.append( emg[0:8] )
			count +=1
		if count>100:
			emg_datarest = np.vstack( emg_datarest )
			print(rehab_lab2_function( emg_datarest)) #every 100 data points collected, call our function
			count = 0
			emg_datarest = []
		
	emg_datarest = np.vstack( emg_datarest )
	print(rehab_lab2_function( emg_datarest))
	print('Done.')
	
	print('Saving file...')
	now = datetime.now()
	timestamp = now.strftime("_%m_%d_%Y__%H_%M")
	savefile = "lab2test"+timestamp+".mat"
	

	sio.savemat(savefile, dict([('EmgDataRest', emg_datarest)])) 
	print('Done.')
	emg_dataclose = []

	
#the following commented out code was what we used to collect 10 seconds of close data after 10 seconds of rest data for part 2 of the lab
'''
t0 = time.time() 

	while time.time() - t0 < run_time:
		emg = myo.state
		if emg is not None:
			emg_dataclose.append( emg[0:8] )

	emg_dataclose = np.vstack( emg_dataclose )
	print('Done.')

	# Save in a .mat file
	print('Saving file...')
	now = datetime.now()
	timestamp = now.strftime("_%m_%d_%Y__%H_%M")
	savefile = "lab2test"+timestamp+".mat"
	

	sio.savemat(savefile, dict([('EmgDataClose', emg_dataclose)])) 
	print('Done.')
'''