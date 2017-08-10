import pprint
import os
import mmap
import datetime
import pandas
import math


from MSProdServerTrace import MSProdServerTrace
from plot import plotLatencies


#CONST
KB = 1024
MB = 1024 * KB
GB = 1024 * MB

#Configuration here
DEV_PATH = '/dev/zero'
DEV_SIZE = 8 * GB
TIME_COMPRESSION = True
DISK_INDEX = 1

def bytesToBlock(val):
	return math.ceil(val / 512)

def blockToBytes(val):
	return math.ceil(val * 512)

def writeToDevice(fd, offset, size):
	startTime = datetime.datetime.now()
	val = os.pwrite(fd, bytearray(size), offset)
	delta = datetime.datetime.now() - startTime
	assert(size == val)
	return getMS(delta)

def readFromDevice(fd, offset, size):
	startTime = datetime.datetime.now()
	val = os.pread(fd, size, offset)
	delta = datetime.datetime.now() - startTime
	assert(size == len(val))
	return getMS(delta)

def getMS(td):
	return td.microseconds + (td.seconds * 1000000) + (td.days * 86400000000)

def runTrace(fd, trace, disk, results):
	#disks = trace.disks()
	#for disk in disks:
	
	dio = trace.diskIO(disk)
	trace = dio['Trace']
	scaleFactor = bytesToBlock(DEV_SIZE) / dio['MaxLBA']

	for index, row in trace.iterrows():
		op = row['Op']
		offset = int(blockToBytes(row['Offset'] * scaleFactor))
		size = int(blockToBytes(row['Size'] * scaleFactor))

		if(op == 'Read'):
			latency = readFromDevice(fd, offset, size)
			#results['Latencies'].append((offset, latency))

		if(op == 'Write'):
			latency = writeToDevice(fd, offset, size)
			#results['Latencies'].append((offset, latency))

		latencyResult = [bytesToBlock(offset), bytesToBlock(size), latency]
		df = pandas.DataFrame([latencyResult], columns=['Offset', 'Size', 'Latency'])
		results['Latencies'] = results['Latencies'].append(df, ignore_index=True)
		#results['Latencies'][index] = latencyResult
		#results['Latencies'].loc[len(results['Latencies'])]=latencyResult

def openDevice(path):
	fd = os.open(path, os.O_RDWR)
	assert(fd >= 1)
	return fd

if __name__ == '__main__':
	fd = openDevice(DEV_PATH)
	pp = pprint.PrettyPrinter(indent=4)
	trace = MSProdServerTrace()
	trace.loadTrace('MSNStorageFileServer-sample.csv', 0)
	results = { 'Latencies': pandas.DataFrame() }

	runTrace(fd, trace, DISK_INDEX, results)
	plotLatencies(results['Latencies'])

