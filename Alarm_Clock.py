#!/usr/bin/python

from threading import Thread
import time
import datetime
class Alarm_Clock:

    def __init__(self,music_player,alarms):
        self.alarms=alarms
        self.music_player=music_player
        t=Thread(target=self.check_alarm,args=())
        t.daemon=True
        t.start()
        

    def check_alarm(self):
        while True:
            for i in range(self.alarms.shape[0]):
                time_str=str(self.alarms.time_h[i])+":"+str(self.alarms.time_min[i])+":00:"+time.strftime("%d:%m:%Y")
                tt = time.mktime(datetime.datetime.strptime(time_str, "%H:%M:%S:%d:%m:%Y").timetuple())
		if round(time.time(),0)==tt:
			if self.alarms.iloc[0]['status']==1:
                        	self.ring_alarm(i)
            time.sleep(1)
   

    def ring_alarm(self,index):
        if self.alarms.iloc[index]['alarm_type']==0:
            self.music_player.play_radio_channel(self.alarms.iloc[index]['media'])

        if self.alarms.iloc[index]['alarm_type']==1:
            self.music_player.stop_music()
            self.music_player.play_single_song(self.alarms.iloc[index]['media'])

