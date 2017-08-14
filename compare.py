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
DEFAULT_TRACE_CUTOFF = 999999999999

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


	#r1 = r1.head(args.traceCutoff)
	#r2 = r2.head(args.traceCutoff)


	#r1['Latency'] = r1['Latency']
	#r2['Latency'] = r2['Latency']


	print(r1.shape)
	print(r2.shape)

	assert (r1.shape == r2.shape)


	print(args.traceResult1, 'mean: ', r1['Latency'].mean(), 'medium', r1['Latency'].median())
	print(args.traceResult1, '05%: ', r1['Latency'].quantile(0.05))
	print(args.traceResult1, '20%: ', r1['Latency'].quantile(0.20))
	print(args.traceResult1, '50%: ', r1['Latency'].quantile(0.50))
	print(args.traceResult1, '80%: ', r1['Latency'].quantile(0.80))
	print(args.traceResult1, '95%: ', r1['Latency'].quantile(0.95))
	print(args.traceResult1, '99%: ', r1['Latency'].quantile(0.99))
	print(args.traceResult1, 'sum:', r1['Latency'].sum())
	print(args.traceResult1, 'size mean:', r1['Size'].mean())

	print(args.traceResult2, 'mean: ', r2['Latency'].mean(), 'medium', r2['Latency'].median())
	print(args.traceResult2, '05%: ', r2['Latency'].quantile(0.05))
	print(args.traceResult2, '20%: ', r2['Latency'].quantile(0.20))
	print(args.traceResult2, '50%: ', r2['Latency'].quantile(0.50))
	print(args.traceResult2, '80%: ', r2['Latency'].quantile(0.80))
	print(args.traceResult2, '95%: ', r2['Latency'].quantile(0.95))
	print(args.traceResult2, '99%: ', r2['Latency'].quantile(0.99))
	print(args.traceResult2, 'sum:', r2['Latency'].sum())
	print(args.traceResult2, 'size mean:', r2['Size'].mean())


	diff = pandas.DataFrame()
	diff['Op'] = r1['Op']
	diff['Offset'] = r1['Offset']
	diff['Size'] = r1['Size']
	diff['Latency'] = r1['Latency'].subtract(r2['Latency'])
	

	#print(diff)

	plotDiff3D(diff)