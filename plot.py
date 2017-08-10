import matplotlib.pyplot as plt
import numpy as np


def plotLatencies(latencyRecords):
	x = latencyRecords['Offset']
	y = latencyRecords['Latency']

	fig = plt.figure()
	ax1 = fig.add_subplot(111)
	
	ax1.plot(x, y, 'ro')

	plt.xlabel('offset')
	plt.ylabel('latency (us)')
	plt.title('test')
	plt.show()