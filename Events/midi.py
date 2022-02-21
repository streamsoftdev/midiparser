#Copyright 2022 Nathan Harwood
#
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.

'''
Created on 15 Sep 2019

@author: julianporter

Updated on 8th Feb 2022

@author: nathan
'''

from .event import Event
from .messages import NoteMessage, PressureMessage, ControlMessage, ProgramMessage, ChannelPressureMessage, PitchBendMessage, SystemMessage

class MIDIEvent(Event):
    
    commands = {
        0x80: 'NOTE_OFF',
        0x90: 'NOTE_ON',
        0xa0: 'PRESSURE',
        0xb0: 'CONTROL_CHANGE',
        0xc0: 'PROGRAM_CHANGE',
        0xd0: 'CHANNEL_PRESSURE',
        0xe0: 'PITCH_BEND'
    }
  
    def __init__(self,time,buffer,current_status):
        super().__init__(time, buffer)
        reduct=0
        if self.header in [0xf1,0xf2,0xf3,0xf4,0xf5,0xf6,
                            0xf8,0xf9,0xfa,0xfb,0xfc,0xfd,0xfe]:
            # system common messages and system real-time messages
            # note that 0xf0 and 0xf7 are handled seperately as SysExEvents
            self.message=SystemMessage(self.buffer)
            self.channel_message = False
        else:
            self.channel_message = True
        if self.channel_message:
            if (self.header & 0b10000000) == 0:
                # for channel messages, i.e. those with a channel number
                # in the header, we use the running status if no status is present
                self.header = current_status 
                self.buffer = buffer
                reduct=-1
        
            self.channel=self.header & 0x0f
            self.command=self.header & 0xf0
            
            if self.command in [0x80,0x90]:
                self.message=NoteMessage(self.command==0x90,self.buffer)
            elif self.command==0xa0:
                self.message=PressureMessage(self.buffer)
            elif self.command==0xb0:
                self.message=ControlMessage(self.buffer)
            elif self.command==0xc0:
                self.message=ProgramMessage(self.buffer)
            elif self.command==0xd0:
                self.message=ChannelPressureMessage(self.buffer)
            elif self.command==0xe0:
                self.message=PitchBendMessage(self.buffer)
            else:
                print("ERROR: unknown MIDI message")

        length = len(self.message) if self.message else 0
        self.data=self.buffer[:length]
        self.length=length+1+reduct
        
    def __str__(self):
        command = self.commands.get(self.command, None)
        if command:
            return f'MIDI@{self.time} {command}[{self.channel}] {self.message}'
        else:
            data = self.stringify(self.data)
            return f'MIDI@{self.time} {self.command}[{self.channel}] {data}'
