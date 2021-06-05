import sys
sys.path.append('c:/EigerPythonDemoScript/')
import time
from DEigerClient import DEigerClient

class Detector:
    def __init__(self, ip, port):
        # DCU network config, please adapt
        self.detector = DEigerClient(ip, port)

    def initialize(self, func):
        self.detector.sendDetectorCommand('initialize')
    
    def setDifferenceModeEnabled(self):
        # Enable difference mode, this disables single threshold mode
        self.detector.setDetectorConfig('threshold/difference/mode', 'enabled')
    
    def setElement(self, elem):
        self.detector.setDetectorConfig('element', str(elem))
        
    def setEnergy(self, energy):
        self.detector.setDetectorConfig('energy', str(energy))
        
    def setFrameTime(self, frameTime):
        self.detector.setDetectorConfig('frame_time', float(frameTime))
        
    def setCountTime(self, countTime):
        self.detector.setDetectorConfig('count_time', float(countTime))
        
    def setNumberTrigger(self, nTrigger):
        self.detector.setDetectorConfig('ntrigger', int(nTrigger))
    
    
    def setLowerThreshold(self, lower):
        self.detector.setDetectorConfig('threshold/1/energy', str(lower))
        
    def setUpperThreshold(self, upper):
        self.detector.setDetectorConfig('threshold/2/energy', str(upper))
    
    def printThresholds(self):
        print('Lower threshold energy: {} eV'.format(self.detector.detectorConfig('threshold/1/energy')['value']))
        print('Upper threshold energy: {} eV'.format(self.detector.detectorConfig('threshold/2/energy')['value']))
    
    def configFileWriter(self, pattern, mode='enabled', imagesPerFile=1000):
        self.detector.setFileWriterConfig('mode', str(mode))
        self.detector.setFileWriterConfig('name_pattern', str(pattern))
        self.detector.setFileWriterConfig('nimages_per_file',int(imagesPerFile))
    
    def armDetector(self):
        self.detector.sendDetectorCommand('arm')
    
    def disarmDetector(self):
        self.detector.sendDetectorCommand('disarm')
    
    def downloadFiles(self, fName, fPath):
        self.detector.fileWriterStatus('data')
        files = [f for f in self.detector.fileWriterStatus('data')['value'] if fName in f]
        for f in files:
            self.detector.fileWriterSave(f, fPath)
            print('\t[OK] %s' %f)
        self.detector.sendFileWriterCommand('clear')
    
