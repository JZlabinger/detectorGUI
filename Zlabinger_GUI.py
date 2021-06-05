# -*- coding: utf-8 -*-
"""
Created on Wed May 26 15:17:41 2021

@author: XRC_Service
"""
import tkinter as tk
from tkinter import scrolledtext
import sys
import threading
sys.path.append('c:/EigerPythonDemoScript/')
from DEigerClient import DEigerClient

DCU_IP = '192.168.42.10'
DCU_PORT = 80
detector = DEigerClient(DCU_IP, DCU_PORT)

DEFAULT_ELEMENT = "Cu"
DEFAULT_ENERGY = ""
DEFAULT_FRAME_TIME = 10
DEFAULT_COUNT_TIME = 8
DEFAULT_NR_TRIGGER = 1
DEFAULT_LOWER_THRESH = ""
DEFAULT_UPPER_THRESH = ""
DEFAULT_NAME_PATTERN = "Pattern_$id"
DEFAULT_PATH = "C:\Eiger_data"
NR_IMAGES_PER_FILE = 1000

all_inputs = []

def printToConsole(text):
    txt_console.config(state=tk.NORMAL)
    txt_console.insert(tk.END, text + '\n')
    txt_console.see('end')
    txt_console.config(state=tk.DISABLED)
    
def disableAllInputs():
    for field in all_inputs:
        field.config(state=tk.DISABLED)
    
def enableAllInputs():
    for field in all_inputs:
        field.config(state=tk.NORMAL)
    
def startThread():
    disableAllInputs()
    global th 
    th = threading.Thread(target=start)
    th.start()

def start():
    printToConsole('Initializing...')
    detector.sendDetectorCommand('initialize')
    printToConsole('Initialized')
    
    # Set detector configuration to external trigger
    detector.setDetectorConfig('trigger_mode', 'exte')
    
    # Set and print element/energy
    if (len(ent_element.get()) != 0):
        printToConsole('Setting Element')
        detector.setDetectorConfig('element', str(ent_element.get()))
        printToConsole("Element: {}".format(detector.detectorConfig('element')['value']))
    else:
        printToConsole('No Element given. Setting energy value')
        detector.setDetectorConfig('photon_energy', float(ent_energy.get()))
    printToConsole("Energy: {} eV".format(detector.detectorConfig('photon_energy')['value']))
    
    # Set and print frame_time and count_time
    detector.setDetectorConfig('frame_time', float(ent_frameTime.get()))
    detector.setDetectorConfig('count_time', float(ent_countTime.get()))
    printToConsole('Frame Time: {}'.format(detector.detectorConfig('frame_time')['value']))
    printToConsole('Count Time: {}'.format(detector.detectorConfig('count_time')['value']))
    
    # Set and print nr of trigger
    nr_trigger = int(ent_nrOfTrigger.get())
    detector.setDetectorConfig('ntrigger', nr_trigger)
    printToConsole('Nr of Trigger: {}'.format(detector.detectorConfig('count_time')['value']))
    
    # Set and print thresholds
    detector.setDetectorConfig('threshold/difference/mode', 'enabled')
    lower_thresh = str(ent_lowerThresh.get())
    upper_thresh = str(ent_upperThresh.get())
    if (len(lower_thresh) != 0):
        detector.setDetectorConfig('threshold/1/energy', lower_thresh)
    if (len(upper_thresh) != 0):
        detector.setDetectorConfig('threshold/2/energy', upper_thresh)
    printToConsole('Lower threshold energy: {} eV'.format(detector.detectorConfig('threshold/1/energy')['value']))
    printToConsole('Upper threshold energy: {} eV'.format(detector.detectorConfig('threshold/2/energy')['value']))
    
    # Configure filewriter
    name_pattern = str(ent_namePattern.get())
    detector.setFileWriterConfig('mode', 'enabled')
    detector.setFileWriterConfig('name_pattern', name_pattern)
    detector.setFileWriterConfig('nimages_per_file', NR_IMAGES_PER_FILE)
    
    # Arm detector and wait for trigger(s)
    printToConsole('Arming detector')
    detector.sendDetectorCommand('arm')
    
    for i in range(nr_trigger):
        if (detector.detectorStatus("state")["value"] == "ready"):
            printToConsole('Waiting for trigger {}'.format(i))
        else:
            printToConsole('Something went wrong. Detector state is "{}" but should be "ready". Detector will now be disarmed.'.format(detector.detectorStatus("state")["value"]))
            break
    printToConsole('Stopping image acquisition')
    printToConsole('Disarming detector')
    detector.sendDetectorCommand('disarm')
    
    fname = name_pattern.replace('$id.*', '')
    fpath = str(lbl_path.get())
    printToConsole('replaced; ' + str(fname))
    download_files(fname, fpath)
        
    enableAllInputs()
    
def download_files(fName, fPath):
    printToConsole('Preparing FileWriter')
    detector.fileWriterStatus('data')
    files = [f for f in detector.fileWriterStatus('data')['value'] if fName in f]
    for f in files:
        detector.fileWriterSave(f, fPath)
        print('\t[OK] %s' %f)
    printToConsole('Clearing buffer')
    detector.sendFileWriterCommand('clear')

# Configure Window
window = tk.Tk()
window.title('Detector Configurator')
window.geometry('800x400')
window.columnconfigure(0, minsize=200, weight=0)
window.columnconfigure(1, minsize=100, weight=1)
window.rowconfigure(0, minsize=100, weight=1)

fr_settings = tk.Frame(window, padx=5)
txt_console = tk.scrolledtext.ScrolledText(window, state=tk.DISABLED)

fr_settings.grid(row=0, column=0, sticky="ns")
txt_console.grid(row=0, column=1, sticky="nsew")

fr_settings.columnconfigure(0, minsize=50, weight=0)
fr_settings.columnconfigure(1, minsize=100, weight=0)

lbl_element = tk.Label(fr_settings, pady=5, padx=5, text="Element:")
ent_element = tk.Entry(fr_settings, width=5)
lbl_element.grid(row=0, column=0, sticky="e")
ent_element.grid(row=0, column=1, sticky="w")
ent_element.insert(tk.END, DEFAULT_ELEMENT)
all_inputs.append(ent_element)

lbl_energy = tk.Label(fr_settings, pady=5, padx=5, text="Energy [eV]:")
ent_energy = tk.Entry(fr_settings, width=10)
lbl_energy.grid(row=1, column=0, sticky="e")
ent_energy.grid(row=1, column=1, sticky="w")
ent_energy.insert(tk.END, DEFAULT_ENERGY)
all_inputs.append(ent_energy)

lbl_frameTime = tk.Label(fr_settings, pady=5, padx=5, text="Frame Time [s]:")
ent_frameTime = tk.Entry(fr_settings, width=10)
lbl_frameTime.grid(row=2, column=0, sticky="e")
ent_frameTime.grid(row=2, column=1, sticky="w")
ent_frameTime.insert(tk.END, DEFAULT_FRAME_TIME)
all_inputs.append(ent_frameTime)

lbl_countTime = tk.Label(fr_settings, pady=5, padx=5, text="Count Time [s]:")
ent_countTime = tk.Entry(fr_settings, width=10)
lbl_countTime.grid(row=3, column=0, sticky="e")
ent_countTime.grid(row=3, column=1, sticky="w")
ent_countTime.insert(tk.END, DEFAULT_COUNT_TIME)
all_inputs.append(ent_countTime)

lbl_nrOfTrigger = tk.Label(fr_settings, pady=5, padx=5, text="Nr of Trigger:")
ent_nrOfTrigger = tk.Entry(fr_settings, width=10)
lbl_nrOfTrigger.grid(row=4, column=0, sticky="e")
ent_nrOfTrigger.grid(row=4, column=1, sticky="w")
ent_nrOfTrigger.insert(tk.END, DEFAULT_NR_TRIGGER)
all_inputs.append(ent_nrOfTrigger)

lbl_lowerThresh = tk.Label(fr_settings, pady=5, padx=5, text="Lower Threshold [eV]:")
ent_lowerThresh = tk.Entry(fr_settings, width=10)
lbl_lowerThresh.grid(row=5, column=0, sticky="e")
ent_lowerThresh.grid(row=5, column=1, sticky="w")
ent_lowerThresh.insert(tk.END, DEFAULT_LOWER_THRESH)
all_inputs.append(ent_lowerThresh)

lbl_upperThresh = tk.Label(fr_settings, pady=5, padx=5, text="Upper Threshold [eV]:")
ent_upperThresh = tk.Entry(fr_settings, width=10)
lbl_upperThresh.grid(row=6, column=0, sticky="e")
ent_upperThresh.grid(row=6, column=1, sticky="w")
ent_upperThresh.insert(tk.END, DEFAULT_UPPER_THRESH)
all_inputs.append(ent_upperThresh)

lbl_namePattern = tk.Label(fr_settings, pady=5, padx=5, text="Name Pattern:")
ent_namePattern = tk.Entry(fr_settings, width=20)
lbl_namePattern.grid(row=7, column=0, sticky="e")
ent_namePattern.grid(row=7, column=1, sticky="w")
ent_namePattern.insert(tk.END, DEFAULT_NAME_PATTERN)
all_inputs.append(ent_namePattern)

lbl_saveLocation = tk.Label(fr_settings, pady=5, padx=5, text="Save location:")
btn_choosePath = tk.Button(fr_settings, text="Choose path")
lbl_path = tk.Label(fr_settings, pady=5, padx=5, wraplength=200, text=DEFAULT_PATH)
lbl_saveLocation.grid(row=8, column=0, sticky="e")
btn_choosePath.grid(row=8, column=1, sticky="w")
lbl_path.grid(row=9, column=0, columnspan=2, sticky="ew")
all_inputs.append(btn_choosePath)

btn_start = tk.Button(fr_settings, width=10, pady=5, padx=5, text="Start Detector", command=startThread)
btn_start.grid(row=10, column=0, columnspan=2, sticky="ew")
all_inputs.append(btn_start)

window.mainloop()