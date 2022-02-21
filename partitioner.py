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
Created on 14 Sep 2019

@author: julianporter

Updated on 20 Feb 2022

@author: nathan
'''

import midiparser.chunks
from midiparser.base import Base
         
class MIDIFile(object):
    
    def __init__(self,filename):
        with open(filename,mode='rb') as file:
            self.bytes=file.read()
        self.header=midiparser.chunks.Header()
        self.tracks=[]
        
    def parse(self):
        buffer=self.bytes
        
        while len(buffer)>8:
            #print("Chunk",[hex(x) for x in buffer[0:8]],[bin(x) for x in buffer[0:8]])
            header=buffer[0:4].decode()
            length=Base.build(buffer[4:8])
            if header=='MThd' : # header
                if length != 6:
                    raise Exception('Header chunk must have length 6')
                self.header = midiparser.chunks.Header(buffer[8:8+length])
                
            elif header=='MTrk' : # track

                self.tracks.append(midiparser.chunks.Track(buffer[8:8+length]))
            else:
                print(f'Unknown chunk type {header} - skipping')
            buffer = buffer[8+length:]
                
    def __str__(self):
        out=[]
        if self.header:
            out.append(str(self.header))
        else:
            out.append('No header!')
        for idx, track in enumerate(self):
            out.append(f'\tTrack {idx} of length {len(track)}')
        return '\n'.join(out)
        
    def __iter__(self):
        return iter(self.tracks)
        
    def __len__(self):
        return len(self.tracks)
        
    def __getitem__(self,index):
        return self.tracks[index]
    
    @property
    def format(self):
        return self.header.format
        
    @property
    def division(self):
        return self.header.division
    
 
    
    
    


           
            
