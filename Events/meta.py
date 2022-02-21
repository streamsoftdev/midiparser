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

Update on 19 Feb 2022

@author: nathan
'''

from collections import OrderedDict
from .event import Event
from midiparser.util import SafeEnum

class MetaEventKinds(SafeEnum):
    
    Sequence_Number = 0
    Text = 1
    Copyright_Notice = 2
    Track_Name = 3
    Instrument_Name = 4
    Lyric = 5
    Marker = 6
    Cue_Point = 7
    MIDI_Channel_Prefix = 0x20
    MIDI_Port_Prefx = 0x21
    End_Of_Track = 0x2f
    Set_Tempo = 0x51
    SMTPE_Offset = 0x54
    Time_Signature = 0x58
    Key_Signature = 0x59
    Sequencer_Specific = 0x7f
    
    def key(self,n):
        if n>=0:
            return ['C','G','D','A','E','B','F#','C#'][n]
        else:
            return ['C','F','Bb','Eb','Ab','Db','Gb','Cb'][-n]
    
    def decode_bcd(self,byte):
        return ((byte&0xf0)>>4)*10+(byte&0x0f)
    
    def attributes(self,_bytes=b''):
        cls=self.__class__
        if self in [cls.Text,cls.Copyright_Notice,cls.Track_Name,cls.Instrument_Name,cls.Lyric,cls.Marker,cls.Cue_Point]:
            return OrderedDict(text = _bytes)
        elif self==cls.Sequence_Number:
            return OrderedDict(number = Event.build(_bytes[:2]))
        elif self==cls.MIDI_Channel_Prefix:
            return OrderedDict(channel = _bytes[0]&0x0f)
        elif self==cls.MIDI_Port_Prefx:
            return OrderedDict(port = _bytes[0]&0xff)
        elif self==cls.End_Of_Track:
            return OrderedDict()
        elif self==cls.Set_Tempo:
            return OrderedDict(tempo = Event.build(_bytes[:3]))
        elif self==cls.SMTPE_Offset:
            return OrderedDict(hh=self.decode_bcd(_bytes[0]),
                mm=self.decode_bcd(_bytes[1]),
                ss=self.decode_bcd(_bytes[2]),
                frame=_bytes[3]+0.01*_bytes[4])
        elif self==cls.Time_Signature:
            return OrderedDict(numerator=_bytes[0],
                denominator=(1<<_bytes[1]),
                clocksPerTick=_bytes[2],
                demisemiquaverPer24Clocks=_bytes[3])
        elif self==cls.Key_Signature:
            mode = { 0 : 'major', 1 : 'minor' }[_bytes[1]]
            return OrderedDict(key=self.key(_bytes[0]),mode=mode)
        elif self==cls.Sequencer_Specific:
            return OrderedDict(data=_bytes)
        else:
            return OrderedDict()
    
class MetaEvent(Event):
    
    def __init__(self,time,buffer):
        super().__init__(time, buffer)
        self.type=self.getInt(1)
        length, n=self.getVarLengthInt()
        self.data=self.getChunk(length)
        self.length=length+n+2
        
        self.message = MetaEventKinds.make(self.type)
        if self.message:
            self.attributes = self.message.attributes(self.data)
    
    def __str__(self):
        if self.message:
            attrs = self.stringify([f'{k}={v}' for k,v in self.attributes.items()])
            return f'META@{self.time} {self.message} -> {attrs}'
        else:
            data = self.stringify(self.data)
            return f'META@{self.time} {self.type} -> {data}'
        

