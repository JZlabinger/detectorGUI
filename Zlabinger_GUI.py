# -*- coding: utf-8 -*-
"""
Created on Wed May 26 15:17:41 2021

@author: XRC_Service
"""
import tkinter as tk
from tkinter import scrolledtext
import sys
sys.path.append('c:/EigerPythonDemoScript/')
import time
import detector_config

DCU_IP = '192.168.42.10'
DCU_PORT = 80
detector = detector_config.Detector(ip=DCU_IP, port=DCU_PORT)

def printToConsole(text):
    txt_console.config(state=tk.NORMAL)
    txt_console.insert(tk.INSERT, text)
    txt_console.config(state=tk.DISABLED)


window = tk.Tk()
window.title('Detector Configurator')
window.geometry('500x500')

window.columnconfigure(0, minsize=100, weight=0)
window.columnconfigure(1, minsize=100, weight=1)
window.rowconfigure(0, minsize=800, weight=1)

fr_settings = tk.Frame(window)
txt_console = tk.scrolledtext.ScrolledText(window, state=tk.DISABLED)

fr_settings.grid(row=0, column=0, sticky="ns")
txt_console.grid(row=0, column=1, sticky="nsew")






window.mainloop()