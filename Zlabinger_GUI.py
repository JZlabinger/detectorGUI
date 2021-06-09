# -*- coding: utf-8 -*-
"""
Created on Wed May 26 15:17:41 2021

@author: XRC_Service
"""
import tkinter as tk
from tkinter import scrolledtext
import sys
import threading
import re
sys.path.append('c:/EigerPythonDemoScript/')
from DEigerClient import DEigerClient

DCU_IP = '192.168.42.10'
DCU_PORT = 80
detector = DEigerClient(DCU_IP, DCU_PORT)

DEFAULT_ELEMENT = "Cu"
DEFAULT_ENERGY = ""
DEFAULT_FRAMETIME = 10
DEFAULT_COUNTTIME = 8
DEFAULT_NR_TRIGGER = 1
DEFAULT_LOWERTHRESH = ""
DEFAULT_UPPERTHRESH = ""
DEFAULT_NAMEPATTERN = "Pattern_$id"
DEFAULT_FPATH = "C:\Eiger_data"
NR_IMAGES_PER_FILE = 1000

all_inputs = []

def printconsole(text):
    txt_console.config(state=tk.NORMAL)
    txt_console.insert(tk.END, text + '\n')
    txt_console.see('end')
    txt_console.config(state=tk.DISABLED)
    
def disable_all_inputs():
    for field in all_inputs:
        field.config(state=tk.DISABLED)
    
def enable_all_inputs():
    for field in all_inputs:
        field.config(state=tk.NORMAL)
    
def startthread():
    disable_all_inputs()
    th = threading.Thread(target=start)
    th.start()

def start():
    printconsole('Initializing...')
    detector.sendDetectorCommand('initialize')
    printconsole('Initialized')
    
    # Set detector configuration to external trigger
    detector.setDetectorConfig('trigger_mode', 'exte')
    
    # Set and print element/energy
    element = str(ent_element.get())
    if (len(element) != 0):
        printconsole('Setting Element')
        detector.setDetectorConfig('element', element)
        printconsole("Element: {}".format(detector.detectorConfig('element')['value']))
    else:
        printconsole('No Element given. Setting energy value')
        detector.setDetectorConfig('photon_energy', float(ent_energy.get()))
    printconsole("Energy: {} eV".format(detector.detectorConfig('photon_energy')['value']))
    
    # Set and print frame_time and count_time
    detector.setDetectorConfig('frame_time', float(ent_frametime.get()))
    detector.setDetectorConfig('count_time', float(ent_counttime.get()))
    printconsole('Frame Time: {}'.format(detector.detectorConfig('frame_time')['value']))
    printconsole('Count Time: {}'.format(detector.detectorConfig('count_time')['value']))
    
    # Set and print nr of trigger
    nr_trigger = int(ent_nr_of_trigger.get())
    detector.setDetectorConfig('ntrigger', nr_trigger)
    printconsole('Nr of Trigger: {}'.format(detector.detectorConfig('count_time')['value']))
    
    # Set and print thresholds
    detector.setDetectorConfig('threshold/difference/mode', 'enabled')
    lowerthresh = str(ent_lowerthresh.get())
    upperthresh = str(ent_upperthresh.get())
    if (len(lowerthresh) != 0):
        detector.setDetectorConfig('threshold/1/energy', lowerthresh)
    if (len(upperthresh) != 0):
        detector.setDetectorConfig('threshold/2/energy', upperthresh)
    printconsole('Lower threshold energy: {} eV'.format(detector.detectorConfig('threshold/1/energy')['value']))
    printconsole('Upper threshold energy: {} eV'.format(detector.detectorConfig('threshold/2/energy')['value']))
    
    # Configure filewriter
    namepattern = str(ent_namepattern.get())
    detector.setFileWriterConfig('mode', 'enabled')
    detector.setFileWriterConfig('namepattern', namepattern)
    detector.setFileWriterConfig('nimages_per_file', NR_IMAGES_PER_FILE)
    
    # Arm detector and wait for trigger(s)
    printconsole('Arming detector')
    detector.sendDetectorCommand('arm')
    
    for i in range(nr_trigger):
        if (detector.detectorStatus("state")["value"] == "ready"):
            printconsole('Waiting for trigger {}'.format(i))
        else:
            printconsole('Something went wrong. Detector state is "{}" but should be "ready". Detector will now be disarmed.'.format(detector.detectorStatus("state")["value"]))
            break
    printconsole('Stopping image acquisition')
    printconsole('Disarming detector')
    detector.sendDetectorCommand('disarm')
    
    fname = re.sub('[$]id.*', '', namepattern)
    fpath = str(lbl_path.cget('text'))
    printconsole('replaced: ' + str(fname))
    downloadfiles(fname, fpath)
        
    enable_all_inputs()
    
def downloadfiles(fname='', fpath=DEFAULT_FPATH):
    try:
        printconsole('Preparing FileWriter')
        detector.fileWriterStatus('data')
        files = [f for f in detector.fileWriterStatus('data')['value'] if fname in f]
        for f in files:
            detector.fileWriterSave(f, fpath)
            print('\t[OK] %s' %f)
        printconsole('Clearing buffer')
        detector.sendFileWriterCommand('clear')
    except:
        exc_tuple = sys.exc_info()
        printconsole("Error:")
        printconsole(str(exc_tuple[0]))
        printconsole(str(exc_tuple[1]))
        printconsole(str(exc_tuple[2]))
    finally:
        printconsole("Done")
        enable_all_inputs()
        return False
    

def downloadfilesmanual():
    disable_all_inputs()
    path = lbl_path.cget('text')
    printconsole(path)
    th = threading.Thread(target= lambda: downloadfiles(fpath=path))
    th.start()


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

lbl_frametime = tk.Label(fr_settings, pady=5, padx=5, text="Frame Time [s]:")
ent_frametime = tk.Entry(fr_settings, width=10)
lbl_frametime.grid(row=2, column=0, sticky="e")
ent_frametime.grid(row=2, column=1, sticky="w")
ent_frametime.insert(tk.END, DEFAULT_FRAMETIME)
all_inputs.append(ent_frametime)

lbl_counttime = tk.Label(fr_settings, pady=5, padx=5, text="Count Time [s]:")
ent_counttime = tk.Entry(fr_settings, width=10)
lbl_counttime.grid(row=3, column=0, sticky="e")
ent_counttime.grid(row=3, column=1, sticky="w")
ent_counttime.insert(tk.END, DEFAULT_COUNTTIME)
all_inputs.append(ent_counttime)

lbl_nr_of_trigger = tk.Label(fr_settings, pady=5, padx=5, text="Nr of Trigger:")
ent_nr_of_trigger = tk.Entry(fr_settings, width=10)
lbl_nr_of_trigger.grid(row=4, column=0, sticky="e")
ent_nr_of_trigger.grid(row=4, column=1, sticky="w")
ent_nr_of_trigger.insert(tk.END, DEFAULT_NR_TRIGGER)
all_inputs.append(ent_nr_of_trigger)

lbl_lowerthresh = tk.Label(fr_settings, pady=5, padx=5, text="Lower Threshold [eV]:")
ent_lowerthresh = tk.Entry(fr_settings, width=10)
lbl_lowerthresh.grid(row=5, column=0, sticky="e")
ent_lowerthresh.grid(row=5, column=1, sticky="w")
ent_lowerthresh.insert(tk.END, DEFAULT_LOWERTHRESH)
all_inputs.append(ent_lowerthresh)

lbl_upperthresh = tk.Label(fr_settings, pady=5, padx=5, text="Upper Threshold [eV]:")
ent_upperthresh = tk.Entry(fr_settings, width=10)
lbl_upperthresh.grid(row=6, column=0, sticky="e")
ent_upperthresh.grid(row=6, column=1, sticky="w")
ent_upperthresh.insert(tk.END, DEFAULT_UPPERTHRESH)
all_inputs.append(ent_upperthresh)

lbl_namepattern = tk.Label(fr_settings, pady=5, padx=5, text="Name Pattern:")
ent_namepattern = tk.Entry(fr_settings, width=20)
lbl_namepattern.grid(row=7, column=0, sticky="e")
ent_namepattern.grid(row=7, column=1, sticky="w")
ent_namepattern.insert(tk.END, DEFAULT_NAMEPATTERN)
all_inputs.append(ent_namepattern)

lbl_savelocation = tk.Label(fr_settings, pady=5, padx=5, text="Save location:")
btn_choosepath = tk.Button(fr_settings, text="Choose path")
lbl_path = tk.Label(fr_settings, pady=5, padx=5, wraplength=200, text=DEFAULT_FPATH)
lbl_savelocation.grid(row=8, column=0, sticky="e")
btn_choosepath.grid(row=8, column=1, sticky="w")
lbl_path.grid(row=9, column=0, columnspan=2, sticky="ew")
all_inputs.append(btn_choosepath)

btn_start = tk.Button(fr_settings, width=15, pady=5, padx=5, text="Start Detector", command=startthread)
btn_start.grid(row=10, column=0, columnspan=2)
all_inputs.append(btn_start)

btn_downloadfiles = tk.Button(fr_settings, width=20, pady=5, padx=5, text="Manually download files", command=downloadfilesmanual)
btn_downloadfiles.grid(row=11, column=0, columnspan=2)
all_inputs.append(btn_downloadfiles)



window.mainloop()