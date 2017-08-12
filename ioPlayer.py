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

def writeToDevice(fd, offset, amountToWrite):
	orgBuf = bytearray(amountToWrite)

	startTime = datetime.datetime.now()

	while(amountToWrite > 0):
		idx = -1 * amountToWrite
		val = os.pwrite(fd, orgBuf[idx:], offset)
		assert(amountToWrite >= val)
		amountToWrite -= val

	delta = datetime.datetime.now() - startTime
	return getMS(delta)

def readFromDevice(fd, offset, amountToRead):
	orgBuf = bytearray(amountToRead)

	startTime = datetime.datetime.now()
	
	while(amountToRead > 0):
		val = os.pread(fd, amountToRead, offset)
		assert(amountToRead >= len(val))
		amountToRead -= len(val)

	delta = datetime.datetime.now() - startTime

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

		if(op == 'Write'):
			latency = writeToDevice(fd, offset, size)

		latencyResult = [bytesToBlock(offset), bytesToBlock(size), latency]
		df = pandas.DataFrame([latencyResult], columns=['Offset', 'Size', 'Latency'])
		results['Latencies'] = results['Latencies'].append(df, ignore_index=True)
		#results['Latencies'][index] = latencyResult
		#results['Latencies'].loc[len(results['Latencies'])]=latencyResult

def openDevice(path):
	fd = os.open(path, os.O_RDWR|os.O_SYNC)
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

