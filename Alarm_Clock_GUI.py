#!/usr/bin/python

from Tkinter import *

class Alarm_Clock_Frames:

	def __init__(self,master,alarm_clock):

		self.alarm_clock=alarm_clock
		self.toplevel_raised=False
		self.alarm_clock_frame=Frame(master)
		self.alarm_clock_frame.grid(row=1,column=0,sticky="nsew")

		# Create Date and Time labels
		self.time_label=Label(self.alarm_clock_frame,text="",font=("Courier",74),justify=CENTER,pady=25)
		self.time_label.pack(fill=X)

		self.date_label=Label(self.alarm_clock_frame,text="",font=("Courier",36),justify=CENTER)
		self.date_label.pack(fill=X)

		# Create Canvas containing alarm list
		self.alarm_clock_view=Frame(self.alarm_clock_frame)
		self.alarm_clock_view.pack(fill=BOTH,expand=True)

		
		self.alarm_clock_label=Label(self.alarm_clock_view,text="00:00",font=("Courier",26),justify=CENTER)
		self.alarm_clock_label.grid(row=0,columnspan=2)

		self.hour_label=Label(self.alarm_clock_view, text="Hour")
		self.hour_label.grid(row=1,column=0)
		self.minute_label=Label(self.alarm_clock_view, text="Minute")
		self.minute_label.grid(row=2,column=0)

		self.entry_hour=Spinbox(self.alarm_clock_view,from_=0,to=23)
		self.entry_hour.grid(row=1,column=1)
		self.entry_minute=Spinbox(self.alarm_clock_view,from_=0,to=59)
		self.entry_minute.grid(row=2,column=1)
	
		self.confirm_alarm_button=Button(self.alarm_clock_view,text="Alarm setzen",command=self.confirm_alarm)
		self.confirm_alarm_button.grid(row=3,column=1)

	
		self.enable_alarm_button=Button(self.alarm_clock_view,text="Alarm ein/aus",command=self.set_alarm)
		self.enable_alarm_button.grid(row=3,column=0)

		self.alarm_status_label=Label(self.alarm_clock_view,text="Alarm ist aus",font=("Courier",18),justify=CENTER)
		self.alarm_status_label.grid(row=4,columnspan=2)		

		self.alarm_clock_view.grid_columnconfigure(0,weight=1)
		self.alarm_clock_view.grid_columnconfigure(1,weight=1)
		

		#Create Alarm Clock control Frame
		self.alarm_clock_control_frame=Frame(master)
		self.alarm_clock_control_frame.grid(row=2,column=0,sticky="nsew")

		self.check_alarm()


	def raise_frames(self):
        	self.alarm_clock_frame.tkraise()
        	self.alarm_clock_control_frame.tkraise()
        


   	def set_time_label(self,label_text):
        	self.time_label.config(text=label_text)
 
	def set_date_label(self,label_text):
        	self.date_label.config(text=label_text)

	def set_alarm_clock_label(self,label_text):
		self.alarm_clock_label.config(text=label_text)
	

	def confirm_alarm(self):
		self.alarm_clock.alarms.at[0,'time_h']=self.entry_hour.get()
		self.alarm_clock.alarms.at[0,'time_min']=self.entry_minute.get()
		self.set_alarm_clock_label(str(self.entry_hour.get())+":"+str(self.entry_minute.get()).zfill(2))
 
	def check_alarm(self):
		self.set_alarm_clock_label(str(self.alarm_clock.alarms.iloc[0]['time_h'])+":"+str(self.alarm_clock.alarms.iloc[0]['time_min']).zfill(2))
		if self.alarm_clock.alarms.iloc[0]['status']==1:
			self.alarm_status_label.config(text="Alarm ist ein")
		else:
			self.alarm_status_label.config(text="Alarm ist aus")

	def set_alarm(self):
		if self.alarm_clock.alarms.iloc[0]['status']==0:
			self.alarm_clock.alarms.at[0,'status']=1
			self.alarm_status_label.config(text="Alarm ist ein")
		else:
			self.alarm_clock.alarms.at[0,'status']=0
			self.alarm_status_label.config(text="Alarm ist aus")


