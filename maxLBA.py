import pprint
import os
import mmap
import datetime
import pandas
import math
from time import sleep
import argparse


from MSProdServerTrace import MSProdServerTrace
from plot import plotLatencies3D


#CONST
KB = 1024
MB = 1024 * KB
GB = 1024 * MB

#Configuration here
DEFAULT_TRACE_FILE_PATH = './traces/MSNStorageFileServer-sample.csv'

def bytesToBlock(val):
	return math.ceil(val / 512)

def blockToBytes(val):
	return math.ceil(val * 512)



class MyParser(argparse.ArgumentParser): 
	def error(self, message):
		sys.stderr.write('error: %s\n' % message)
		self.print_help()
		sys.exit(2)


def saveLatencyResults(fileName, results):
	with open(fileName, 'a') as f:
		results['Latencies'].to_csv(f, sep=',', header=False, index=False)

if __name__ == '__main__':
	parser = MyParser()
	parser.add_argument("-tf", "--traceFilePath", help="trace file path", type=str, default=DEFAULT_TRACE_FILE_PATH, required=False)
	
	args = parser.parse_args()

	print('traceFilePath:', args.traceFilePath)

	pp = pprint.PrettyPrinter(indent=4)

	trace = MSProdServerTrace()
	trace.loadTrace(args.traceFilePath, 0)	