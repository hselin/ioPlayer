
import pandas
import numpy
import pprint

class Trace(object):
    def __init__(self):
        self.name = "moo"

    def loadTrace(self, filePath):
        return

    def reset(self):
        return

class MSProdServerTrace(Trace):
    def __init__(self):
        self.name = "MSProdServerTrace"
        self.reset()

    def loadTrace(self, filePath, timeOffset):
        names = ['Op', 'Time', 'PID', 'TID', 'IrpPtr', 'Offset', 'Size', 'ElapsedTime', 'Disk', 'IrpFlags', 'DiskSvcTime', 'Prio', 'VolSnap', 'FileObj', 'FileName']
        usecols = ['Op', 'Time', 'Offset', 'Size', 'Disk']
        df = pandas.read_csv(filePath, names=names, usecols=usecols, header='infer')

        df['Op'] = df['Op'].str.strip().replace('DiskRead', 'Read')
        df['Op'] = df['Op'].str.strip().replace('DiskWrite', 'Write')
        df['Op'] = df['Op'].str.strip().replace('DiskFlush', 'Flush')

        df = df[pandas.notnull(df['Time'])]
        #df = df[pandas.notnull(df['Offset'])]
        #df = df[pandas.notnull(df['Size'])]
        #df = df[pandas.notnull(df['Disk'])]
        df = df[df['Time'].str.strip()!='TimeStamp']
        
        opList = ['Read', 'Write', 'Flush']
        df = df[df.Op.isin(opList)]

        df['Time'] = df['Time'].apply(lambda x: int(x))
        df['Offset'] = df['Offset'].apply(lambda x: 0 if x==' ' else (int(x, 16) / 512))
        df['Size'] = df['Size'].apply(lambda x: 0 if x==' ' else (int(x, 16) / 512))
        #df['Offset'] = df['Offset'].apply(lambda x: int(x, 16) / 512)
        #df['Size'] = df['Size'].apply(lambda x: int(x, 16) / 512)
        df['Disk'] = df['Disk'].apply(lambda x: int(x))
        df['End'] = df['Offset'] + df['Size'] - 1

        for disk in df.Disk.unique():
            if(self.ios.get(disk) == None):
                self.ios[disk] = {}
                self.ios[disk]['Trace'] = pandas.DataFrame()
                self.ios[disk]['MaxLBA'] = 0

            self.ios[disk]['Trace'] = self.ios[disk]['Trace'].append(df[df['Disk']==disk], ignore_index=True)
            self.ios[disk]['Trace'] = self.ios[disk]['Trace'].sort_values(['Time'], ascending=[True])
            maxLBA = self.ios[disk]['Trace']['End'].max() 
            self.ios[disk]['MaxLBA'] = max(self.ios[disk]['MaxLBA'], maxLBA)

        self.endTime = df['Time'].max() + timeOffset
        self.startTime = df['Time'].min() + timeOffset

        print(df)

    def reset(self):
        self.ios = {}
        self.startTime = 0
        self.endTime = 0
        self.maxLBA = 0

    def disks(self):
        return self.ios.keys()

    def diskIO(self, disk):
        return self.ios[disk]

