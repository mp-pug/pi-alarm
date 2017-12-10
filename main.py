#!/usr/bin/python

from Tkinter import *
import vlc
import time
import os 
import pandas as pd
from threading import Thread
import Music_Player
import Alarm_Clock
import Alarm_Clock_GUI
import Music_Player_GUI


  
def update_time(timelabel,datelabel,Alarm_Clock_Frame):
    while True:
        timelabel.config(text=time.strftime("%H:%M:%S"))
        datelabel.config(text=time.strftime("%d.%m.%Y"))
        Alarm_Clock_Frame.set_time_label(time.strftime("%H:%M:%S"))
        Alarm_Clock_Frame.set_date_label(time.strftime("%d.%m.%Y"))
        time.sleep(1)




channel_csv_file="channels.csv"
host_file="hosts.csv"
alarm_file="alarm.csv"
ch_df=pd.read_csv(channel_csv_file)

alarms=pd.read_csv(alarm_file)



media_root_directory="/"
terminate_flag=False

music_player=Music_Player.Music_Player()
alarm_clock=Alarm_Clock.Alarm_Clock(music_player,alarms)



# Create the GUI
root=Tk()
root.resizable(width=False, height=False)
root.geometry('{}x{}'.format(800,480))

alarm_clock_frames=Alarm_Clock_GUI.Alarm_Clock_Frames(root,alarm_clock)

# Create Music Player Frames
music_player_frames=Music_Player_GUI.Music_Player_Frames(root,music_player,media_root_directory,ch_df)

root.grid_columnconfigure(0,weight=1)

# Create Date Label and menu
status_frame=Frame(root)
status_frame.grid(row=0,column=0,sticky="nsew")

# Create the menu to switch between alarm clock, radio and mp3
category_frame=Frame(status_frame)
category_frame.pack(side=LEFT)


alarm_clock_cat=Button(category_frame,text="Wecker",command=alarm_clock_frames.raise_frames)
alarm_clock_cat.grid(row=0,column=2)


radio_cat=Button(category_frame,text="Radio",command=music_player_frames.raise_radio_frames)
radio_cat.grid(row=0,column=4)

date_label= Label(status_frame,text=time.strftime("%d.%m.%Y"))
date_label.pack(side=RIGHT)

time_label= Label(status_frame,text=time.strftime("%H:%M:%S"))
time_label.pack(side=RIGHT)


music_player_frames.raise_radio_frames()

try:
    t=Thread(target=update_time,args=(time_label,date_label,alarm_clock_frames,))
    t.daemon=True
    t.start()
except (KeyboardInterrupt,SystemExit):
        t.stop()
        sys.exit()

root.mainloop()
alarms.to_csv(alarm_file,header='column_names',index=False)
