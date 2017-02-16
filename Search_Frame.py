#!/usr/bin/python


from Tkinter import *


class Search_Frame:

    def __init__(self,master,mediathek_root_directory,channel_csv_file):

        # Create Search frame
        self.search_frame=Frame(master)
        self.search_frame.grid(row=1,column=0,sticky="nsew")

        self.search_control_frame=Frame(master)
        self.search_control_frame.grid(row=2,column=0,sticky="nsew")




    def raise_frames(self):
        self.search_frame.tkraise()
        self.search_control_frame.tkraise()
