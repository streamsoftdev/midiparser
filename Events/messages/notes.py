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
Created on 16 Sep 2019

@author: julianporter

Update on 7th Feb 2022

@author: nathan
'''
from midiparser.base import MIDIParserError
import re

class Note(object):
    
    notes=['c','c#','d','d#','e','f','f#','g','g#','a','a#','b']
    
    def _fromNumber(self,n):
        number=n&0xff
        self.note_num=number
        self.note=self.notes[number % 12]
        self.octave=number//12
        
    def _fromString(self,s):
        match=re.fullmatch('([a-g]{1}[\#]?)([\d]{1,2})',s,flags=re.RegexFlag.IGNORECASE)
        if not match:
            raise MIDIParserError(f'Invalid note label {s}')
        n, o = match.groups() 
        self.note=self.notes.index(n.lower())
        self.octave=int(o)
        
    def _fromPitchAndOctave(self,pitch,octave):
        if pitch<0 or octave<0:
            raise MIDIParserError('pitch and octave must be non-negative')
        self.note=int(pitch)%12
        self.octave=octave
    
    def __init__(self,*args,**kwargs):
        if len(args)>0:
            arg=args[0]
            if type(arg)==int:
                self._fromNumber(arg)
            elif type(arg)==str:
                self._fromString(arg)
            else:
                raise MIDIParserError(f'Cannot parse note string {arg}') 
        elif 'pitch' in kwargs and 'octave' in kwargs:
            self._fromPitchAndOctave(kwargs['pitch'],kwargs['octave'])
        else:
            raise MIDIParserError('illegal arguments for MIDI Note')    
        
    @property
    def number(self):
        if type(self.note)==int:
            note_number = self.note+self.octave*12
        else:
            note_number = self.notes.index(self.note)+self.octave*12
        return note_number
    
    def __str__(self):
        return f'{self.note.upper()}{self.octave}'
    
class NoteMessage(object):
    
    def __init__(self,onOff,data=b''):
        self.onOff='ON' if onOff else 'OFF'
        self.note=Note(data[0])
        self.velocity=data[1]
        
    def __str__(self):
        return f'{self.note} {self.onOff} velocity := {self.velocity}'
    
    def __len__(self):
        return 2
    
class PressureMessage(object):
    
    def __init__(self,data=b''):
        self.note=Note(data[0])
        self.pressure=data[1]
        
    def __str__(self):
        return f'{self.note} pressure := {self.pressure}'
    
    def __len__(self):
        return 2
    
    
