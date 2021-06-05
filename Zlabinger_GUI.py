# -*- coding: utf-8 -*-
"""
Created on Wed May 26 15:17:41 2021

@author: XRC_Service
"""
import tkinter as tk
import sys
sys.path.append('c:/EigerPythonDemoScript/')
import time
import detector_config

DCU_IP = '192.168.42.10'
DCU_PORT = 80
detector = detector_config.Detector(ip=DCU_IP, port=DCU_PORT)

def printToConsole(text):
    txt_console.config(state=tk.NORMAL)
    txt_console.insert(tk.INSERT, text + '\n')
    txt_console.config(state=tk.DISABLED)
    
def start():
    printToConsole('Initializing...')
    #detector.initialize(printToConsole)
    printToConsole('Initialized')
    
    return True
    

# Configure Window
window = tk.Tk()
window.title('Detector Configurator')
window.geometry('500x500')
window.columnconfigure(0, minsize=200, weight=0)
window.columnconfigure(1, minsize=100, weight=1)
window.rowconfigure(0, minsize=800, weight=1)

fr_settings = tk.Frame(window)
txt_console = tk.scrolledtext.ScrolledText(window, state=tk.DISABLED)

fr_settings.grid(row=0, column=0, sticky="ns")
txt_console.grid(row=0, column=1, sticky="nsew")

fr_settings.columnconfigure(0, minsize=50, weight=0)
fr_settings.columnconfigure(1, minsize=100, weight=0)

lbl_element = tk.Label(fr_settings, pady=5, padx=5, text="Element:")
ent_element = tk.Entry(fr_settings, width=5)
lbl_element.grid(row=0, column=0, sticky="e")
ent_element.grid(row=0, column=1, sticky="w")

lbl_energy = tk.Label(fr_settings, pady=5, padx=5, text="Energy:")
ent_energy = tk.Entry(fr_settings, width=10)
lbl_energy.grid(row=1, column=0, sticky="e")
ent_energy.grid(row=1, column=1, sticky="w")

lbl_frameTime = tk.Label(fr_settings, pady=5, padx=5, text="Frame Time:")
ent_frameTime = tk.Entry(fr_settings, width=10)
lbl_frameTime.grid(row=2, column=0, sticky="e")
ent_frameTime.grid(row=2, column=1, sticky="w")

lbl_countTime = tk.Label(fr_settings, pady=5, padx=5, text="Count Time:")
ent_countTime = tk.Entry(fr_settings, width=10)
lbl_countTime.grid(row=3, column=0, sticky="e")
ent_countTime.grid(row=3, column=1, sticky="w")

lbl_nrOfTrigger = tk.Label(fr_settings, pady=5, padx=5, text="Nr of Trigger:")
ent_nrOfTrigger = tk.Entry(fr_settings, width=10)
lbl_nrOfTrigger.grid(row=4, column=0, sticky="e")
ent_nrOfTrigger.grid(row=4, column=1, sticky="w")

lbl_lowerThresh = tk.Label(fr_settings, pady=5, padx=5, text="Lower Threshold:")
ent_lowerThresh = tk.Entry(fr_settings, width=10)
lbl_lowerThresh.grid(row=5, column=0, sticky="e")
ent_lowerThresh.grid(row=5, column=1, sticky="w")

lbl_upperThresh = tk.Label(fr_settings, pady=5, padx=5, text="Upper Threshold:")
ent_upperThresh = tk.Entry(fr_settings, width=10)
lbl_upperThresh.grid(row=6, column=0, sticky="e")
ent_upperThresh.grid(row=6, column=1, sticky="w")

lbl_saveLocation = tk.Label(fr_settings, pady=5, padx=5, text="Save location:")
btn_choosePath = tk.Button(fr_settings, text="Choose path")
lbl_path = tk.Label(fr_settings, pady=5, padx=5, wraplength=200, text="Your/Path")
lbl_saveLocation.grid(row=7, column=0, sticky="e")
btn_choosePath.grid(row=7, column=1, sticky="w")
lbl_path.grid(row=8, column=0, columnspan=2, sticky="ew")

btn_start = tk.Button(fr_settings, width=10, pady=5, padx=5, text="Start Detector", command=start)
btn_start.grid(row=9, column=0, columnspan=2, sticky="ew")

window.mainloop()