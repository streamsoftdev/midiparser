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

Update on 7th Feb 2022

@author: nathan
'''

from .chunk import Chunk
from midiparser.Events import MetaEvent, MIDIEvent, SysExEvent
import traceback
           

class Track(Chunk):
    
    def __init__(self,data,containsTiming = True):
        super().__init__(data)
        self.events=[]
        self.containsTiming = containsTiming
           
    def parse(self):
        self.buffer=self.data
        time=0 if self.containsTiming else None
        #print("Track header",[hex(x) for x in self.buffer[0:8]],[bin(x) for x in self.buffer[0:8]])
        current_status=None
        events=0
        try:
            #print("Starting to parse track")
            #print("=======================")
            while len(self.buffer)>0 :
                #print([hex(x) for x in self.buffer[:20]])
                #print(f'Parsing {len(self.buffer)} bytes')
                if self.containsTiming:
                    delta, _=self.getVarLengthInt()
                    time+=delta
                #print(f'Time is {time} length {n}')
                if len(self.buffer)==0:
                    # timing information with no event ... possible parsing error
                    print("Warning: possible parsing error.")
                    break
            
                eventType=self.buffer[0]
                
                #print(f'Event type is {eventType}')
                if eventType == 0xff:     # Meta event
                    event = MetaEvent(time,self.buffer)
                    #print(event)
                elif eventType in [0xf0,0xf7]: # Sysex event
                    event = SysExEvent(time,self.buffer)
                elif not ((current_status == None) and ((eventType&0b10000000) == 0)):
                    event = MIDIEvent(time,self.buffer,current_status)
                    if event.channel_message:
                        current_status = event.header
                    #print(event)
                else:
                    print("ERROR: malformed event.")
                    break
                    
                
                
                length = len(event)
                self.events.append(event)
                self.buffer=self.buffer[length:]
                #events+=1
                #print(event)
                #if events>200:
                #    break

        except Exception:
            #print(f'Error : {e}')
            traceback.print_exc()
            pass
    
    def __iter__(self):
        return iter(self.events)
        
    def __len__(self):
        return len(self.events)
        
    def __getitem__(self,index):
        return self.events[index]
    
    def __str__(self):
        return self.stringify(self.events, '\n')
        
