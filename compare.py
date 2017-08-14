import pprint
import os
import mmap
import datetime
import pandas
import math
from time import sleep
import argparse
import sys
from plot import plotDiff3D

DEFAULT_TRACE_RESULT = 'out.csv'
DEFAULT_TRACE_CUTOFF = 500000

class MyParser(argparse.ArgumentParser): 
	def error(self, message):
		sys.stderr.write('error: %s\n' % message)
		self.print_help()
		sys.exit(2)

def loadTraceResult(filePath):
	names = ['Op', 'Offset', 'Size', 'Latency']

	dtype={"Op": str, 'Offset': str, 'Size': str, 'Latency': str}

	df = pandas.read_csv(filePath, names=names, header='infer', dtype=dtype)


	df['Offset'] = df['Offset'].apply(lambda x: int(x))
	df['Size'] = df['Size'].apply(lambda x: int(x))
	df['Latency'] = df['Latency'].apply(lambda x: int(x))


	return df

if __name__ == '__main__':
	parser = MyParser()
	parser.add_argument("-tr1", "--traceResult1", help="trace result 1", type=str, default=DEFAULT_TRACE_RESULT, required=False)
	parser.add_argument("-tr2", "--traceResult2", help="trace result 2", type=str, default=DEFAULT_TRACE_RESULT, required=False)
	parser.add_argument("-tc", "--traceCutoff", help="trace result cutoff", type=int, default=DEFAULT_TRACE_CUTOFF, required=False)
	
	args = parser.parse_args()

	print('traceResult1:', args.traceResult1)
	print('traceResult2:', args.traceResult2)
	print('traceCutoff:', args.traceCutoff)


	r1 = loadTraceResult(args.traceResult1)
	r2 = loadTraceResult(args.traceResult2)


	r1 = r1.head(args.traceCutoff)
	r2 = r2.head(args.traceCutoff)

	print(r1.shape)
	print(r2.shape)


	assert (r1.shape == r2.shape)

	diff = pandas.DataFrame()
	diff['Op'] = r1['Op']
	diff['Offset'] = r1['Offset']
	diff['Size'] = r1['Size']
	diff['Latency'] = r1['Latency'].subtract(r2['Latency'])
	

	print(diff)

	plotDiff3D(diff)