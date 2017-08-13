import pprint
import os
import mmap
import datetime
import pandas
import math
from time import sleep
import argparse


from MSProdServerTrace import MSProdServerTrace
from plot import plotLatencies


#CONST
KB = 1024
MB = 1024 * KB
GB = 1024 * MB

#Configuration here
DEFAULT_DEV_PATH = '/dev/zero'
DEFAULT_DEV_SIZE = 8 * GB
DEFAULT_DISK_INDEX = 1
DEFAULT_TRACE_FILE_PATH = './traces/MSNStorageFileServer-sample.csv'

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
	return getTotalUS(delta)

def readFromDevice(fd, offset, amountToRead):
	orgBuf = bytearray(amountToRead)

	startTime = datetime.datetime.now()
	
	while(amountToRead > 0):
		val = os.pread(fd, amountToRead, offset)
		assert(amountToRead >= len(val))
		amountToRead -= len(val)

	delta = datetime.datetime.now() - startTime

	return getTotalUS(delta)

def flushDevice(fd):
	startTime = datetime.datetime.now()

	os.flush(fd)

	delta = datetime.datetime.now() - startTime

	return getTotalUS(delta)

def getTotalUS(td):
	return (td.microseconds + (td.seconds * 1000000) + (td.days * 86400000000))

def usToSec(us):
	return (us / 1000000)

def adaptiveSleep(us):
	if(us >= 10000):
		sleep(usToSec(us))
	else:
		startTime = datetime.datetime.now()
		while (getTotalUS(datetime.datetime.now() - startTime) < us):
			pass


def runTrace(fd, devSize, trace, disk, timeCompression, results):
	#disks = trace.disks()
	#for disk in disks:
	
	dio = trace.diskIO(disk)
	trace = dio['Trace']
	scaleFactor = bytesToBlock(devSize) / dio['MaxLBA']

	runStartTime = datetime.datetime.now()


	print(trace.shape)

	for index, row in trace.iterrows():
		op = row['Op']
		offset = int(blockToBytes(row['Offset'] * scaleFactor))
		size = int(blockToBytes(row['Size'] * scaleFactor))
		cmdTime = row['Time']

		if not timeCompression:
			while True:
				elapsedTime = getTotalUS(datetime.datetime.now() - runStartTime)
				#print(index, cmdTime - elapsedTime)
				if(elapsedTime < cmdTime):
					adaptiveSleep(cmdTime - elapsedTime)
				else:
					break

		if((index % 100) == 0):
			print(index)

		if(op == 'Read'):
			latency = readFromDevice(fd, offset, size)

		elif(op == 'Write'):
			latency = writeToDevice(fd, offset, size)
		
		elif(op == 'Flush'):
			latency = flushDevice(fd)

		latencyResult = [bytesToBlock(offset), bytesToBlock(size), latency]
		df = pandas.DataFrame([latencyResult], columns=['Offset', 'Size', 'Latency'])
		results['Latencies'] = results['Latencies'].append(df, ignore_index=True)


def openDevice(path):
	#fd = os.open(path, os.O_RDWR|os.O_SYNC)
	fd = os.open(path, os.O_RDWR)
	assert(fd >= 1)
	return fd

def closeDevice(fd):
	os.close(fd)


class MyParser(argparse.ArgumentParser): 
	def error(self, message):
		sys.stderr.write('error: %s\n' % message)
		self.print_help()
		sys.exit(2)


if __name__ == '__main__':
	parser = MyParser()
	parser.add_argument("-d", "--devPath", help="device path", type=str, default=DEFAULT_DEV_PATH, required=False)
	parser.add_argument("-s", "--devSize", help="device size", type=int, default=DEFAULT_DEV_SIZE, required=False)
	parser.add_argument("-tc", "--timeCompression", help="turn on time compression", action='store_true', required=False)
	parser.add_argument("-i", "--diskIndex", help="disk index", type=int, default=DEFAULT_DISK_INDEX, required=False)
	parser.add_argument("-tf", "--traceFilePath", help="trace file path", type=str, default=DEFAULT_TRACE_FILE_PATH, required=False)
	parser.add_argument("-p", "--plotData", help="plot resulting data", action='store_true', required=False)
	
	args = parser.parse_args()

	print('devPath:', args.devPath)
	print('devSize:', args.devSize)
	print('timeCompression:', args.timeCompression)
	print('diskIndex:', args.diskIndex)
	print('traceFilePath:', args.traceFilePath)
	print('plotData:', args.plotData)


	pp = pprint.PrettyPrinter(indent=4)

	fd = openDevice(args.devPath)

	trace = MSProdServerTrace()
	trace.loadTrace(args.traceFilePath, 0)
	results = { 'Latencies': pandas.DataFrame() }

	runTrace(fd, args.devSize, trace, args.diskIndex, args.timeCompression, results)

	closeDevice(fd)

	if (args.plotData):
		plotLatencies(results['Latencies'])