#!/usr/bin/python

from Tkinter import *

class Alarm_Clock_Frame:

    def __init__(self,master):
        self.alarm_clock_frame=Frame(master)
        self.alarm_clock_frame.grid(row=1,column=0,sticky="nsew")

        #Create Alarm Clock control Frame
        self.alarm_clock_control_frame=Frame(master)
        self.alarm_clock_control_frame.grid(row=2,column=0,sticky="nsew")


    def raise_frames(self):
        self.alarm_clock_frame.tkraise()
        self.alarm_clock_control_frame.tkraise()
