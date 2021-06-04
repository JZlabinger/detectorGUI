import sys
sys.path.append('c:/EigerPythonDemoScript/')
import time
from DEigerClient import DEigerClient
# DCU network config, please adapt
DCU_IP = '192.168.42.10'
DCU_PORT = 80
detector = DEigerClient(DCU_IP, DCU_PORT)

if (False):
    detector.fileWriterStatus('data')
    fname = '3trigger'
    fpath = 'c:\Eiger_data'
    files = [f for f in detector.fileWriterStatus('data')['value'] if fname in f]
    for f in files:
        detector.fileWriterSave(f, fpath)
        print '\t[OK] %s' %f
    detector.sendFileWriterCommand('clear')

#detector.setDetectorConfig("trigger_mode", "inte")

if (False):
    print('{}'.format(detector.detectorStatus("state")))
    print('{}'.format(detector.detectorConfig("trigger_mode")))
    print('{}'.format(detector.detectorConfig("ntrigger")))
    #print('{}'.format(detector.detectorConfig("threshold/1/energy")))
    #print('{}'.format(detector.detectorConfig("threshold/2/energy")))
    print('{}'.format(detector.fileWriterConfig("nimages_per_file")))
    print('{}'.format(detector.fileWriterStatus("data")))

if (False):
    while (True):
        print('{}'.format(detector.detectorStatus("state")))
        time.sleep(2)

if (True):
    detector.sendFileWriterCommand('clear')