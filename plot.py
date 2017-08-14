import matplotlib
#matplotlib.use('GTKAgg')
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D



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

def plotLatencies3D(latencyRecords):
	fig = plt.figure()
	ax = Axes3D(fig)

	reads = latencyRecords[latencyRecords['Op'] == 'Read']
	writes = latencyRecords[latencyRecords['Op'] == 'Write']

	xr = reads['Offset']
	yr = reads['Size']
	zr = reads['Latency']

	xw = writes['Offset']
	yw = writes['Size']
	zw = writes['Latency']



	ax.scatter(xr, yr, zr, c='b', marker='o')
	ax.scatter(xw, yw, zw, c='r', marker='o')


	plt.xlabel('Offset (LBA)')
	plt.ylabel('Size (blks)')
	ax.set_zlabel('Latency (us)')

	plt.show()

def plotDiff3D(latencyDiffRecords):
	positives = latencyDiffRecords[latencyDiffRecords['Latency'] >= -1000]
	negatives = latencyDiffRecords[latencyDiffRecords['Latency'] < -1000]

	xp = positives['Offset']
	yp = positives['Size']
	zp = positives['Latency']

	xn = negatives['Offset']
	yn = negatives['Size']
	zn = negatives['Latency']

	print('# of positives: ', len(zp), len(zp) / (len(zp) + len(zn)))
	print('# of negatives: ', len(zn), len(zn) / (len(zp) + len(zn)))



	fig = plt.figure()
	ax = Axes3D(fig)

	ax.scatter(xp, yp, zp, c='b', marker='o')
	ax.scatter(xn, yn, zn, c='r', marker='o')


	plt.xlabel('Offset (LBA)')
	plt.ylabel('Size (blks)')
	ax.set_zlabel('Latency (us)')

	plt.show()