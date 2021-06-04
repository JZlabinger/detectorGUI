import sys
sys.path.append('c:/EigerPythonDemoScript/')
import time
from DEigerClient import DEigerClient
# DCU network config, please adapt
DCU_IP = '192.168.42.10'
DCU_PORT = 80
detector = DEigerClient(DCU_IP, DCU_PORT)

def initDetector():
    print('Initializing...')
    detector.sendDetectorCommand('initialize')
    print('Initialized')

# First initialize the detector
initDetector()

# Set detector configuration, see API reference section 4.1.1
detector.setDetectorConfig('element', 'Cu')
detector.setDetectorConfig('frame_time', 0.025)
detector.setDetectorConfig('count_time', 0.010)
detector.setDetectorConfig('ntrigger', 1)

# Enable difference mode, this disables single threshold mode
detector.setDetectorConfig('threshold/difference/mode', 'enabled')

# Set threshold Energies
#detector.setDetectorConfig('threshold/1/energy', '4000')
#detector.setDetectorConfig('threshold/2/energy', '11000')

# Check threshold settings
print('Lower threshold energy: {} eV'.format(detector.detectorConfig('threshold/1/energy')['value']))
print('Upper threshold energy: {} eV'.format(detector.detectorConfig('threshold/2/energy')['value']))

# Configure filewriter
detector.setFileWriterConfig('mode', 'enabled')
detector.setFileWriterConfig('name_pattern', '1_1trigger2_$id')
detector.setFileWriterConfig('nimages_per_file', 1000)

# Make image acquisition
print('Taking image')
detector.sendDetectorCommand('arm')
detector.sendDetectorCommand('trigger')
detector.sendDetectorCommand('disarm')
print('Taking image 2')
detector.sendDetectorCommand('arm')
detector.sendDetectorCommand('trigger')
detector.sendDetectorCommand('disarm')
print('Taking image 3')
detector.sendDetectorCommand('arm')
detector.sendDetectorCommand('trigger')
detector.sendDetectorCommand('disarm')
print('Taking image 4')
detector.sendDetectorCommand('arm')
detector.sendDetectorCommand('trigger')
detector.sendDetectorCommand('disarm')
print('Taking image 5')
detector.sendDetectorCommand('arm')
detector.sendDetectorCommand('trigger')
detector.sendDetectorCommand('disarm')
print('Acquisition finished')
time.sleep(2)

# we try to download files
detector.fileWriterStatus('data')
fname = '1_1trigger'
fpath = 'c:\Eiger_data'
files = [f for f in detector.fileWriterStatus('data')['value'] if fname in f]
for f in files:
    detector.fileWriterSave(f, fpath)
    print '\t[OK] %s' %f
detector.sendFileWriterCommand('clear')
#detector.fileWriterFiles('iron_source6', 'DELETE')