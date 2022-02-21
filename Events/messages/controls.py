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

Update on 20 Feb 2022

@author: nathan
'''


from .converters import ConversionEnum, Converter


def Pedals(data):
    x = data[0]
    onOff = 'OFF' if x<64 else 'ON'
    return onOff

class ControlMessages(ConversionEnum):
    Bank_Select_MSB = 0
    Modulation_Wheel_MSB = 1 # vibrato
    Breath_Controller_MSB = 2
    Undefined_1 = 3
    Foot_Pedal_MSB = 4 # how the foot pedal is used
    Portamento_Time_MSB = 5 # rate to slide between 2 notes played subsequently
    Data_Entry_MSB = 6
    Channel_Volume_MSB = 7
    Balance_MSB = 8 # left and right balance for stereo patch, 64 is center
    Undefined_2 = 9
    Pan_MSB = 10 # for mono patches, 64 is center
    Expression_MSB = 11 # percentage of volume
    Effect_Controller_1_MSB = 12
    Effect_Controller_2_MSB = 13
    Undefined_3 = 14
    Undefined_4 = 15
    General_Purpose_1 = 16
    General_Purpose_2 = 17
    General_Purpose_3 = 18
    General_Purpose_4 = 19
    Undefined_5 = 20
    Undefined_6 = 21
    Undefined_7 = 22
    Undefined_8 = 23
    Undefined_9 = 24
    Undefined_10 = 25
    Undefined_11 = 26
    Undefined_12 = 27
    Undefined_13 = 28
    Undefined_14 = 29
    Undefined_15 = 30
    Undefined_16 = 31
    Bank_Select_LSB = 32 
    Modulation_Wheel_LSB = 33
    Breath_Controller_LSB = 34
    Undefined_1_LSB = 35
    Foot_Pedal_LSB = 36
    Portamento_Time_LSB = 37
    Data_Entry_LSB = 38
    Channel_Volume_LSB = 39
    Balance_LSB = 40
    Undefined_2_LSB = 41
    Pan_LSB = 42
    Expression_LSB = 43
    Effect_Controller_1_LSB = 44
    Effect_Controller_2_LSB = 45
    Undefined_17 = 46
    Undefined_18 = 47
    Undefined_19 = 48
    Undefined_20 = 49
    Undefined_21 = 50
    Undefined_22 = 51
    Undefined_23 = 52
    Undefined_24 = 53
    Undefined_25 = 54
    Undefined_26 = 55
    Undefined_27 = 56
    Undefined_28 = 57
    Undefined_29 = 58
    Undefined_30 = 59
    Undefined_31 = 60
    Undefined_32 = 61
    Undefined_33 = 62
    Undefined_34 = 63
    Damper_Pedal = (64,Pedals) # when on, holds (sustains) notes that are playing or played, even if the note is released, until it switches off
    Portamento_Pedal = (65,Pedals) 
    Sostenuto_Pedal = (66,Pedals) # only holds notes that were on when the pedal was pressed
    Soft_Pedal = (67,Pedals) # lowers the volume of notes played
    Legato_Pedal = (68,Pedals) # 
    Hold_2 = (69,Pedals)
    Sound_Variation = 70
    Sound_Timbre = 71
    Sound_Release_Time = 72
    Sound_Attack_Time = 73
    Sound_Brightness = 74
    Sound_Control_6 = 75
    Sound_Control_7 = 76
    Sound_Control_8 = 77
    Sound_Control_9 = 78
    Sound_Control_10 = 79
    General_Purpose_Button_1 = (80,Pedals)
    General_Purpose_Button_2 = (81,Pedals)
    General_Purpose_Button_3 = (82,Pedals)
    General_Purpose_Button_4 = (83,Pedals)
    Undefined_35 = 84
    Undefined_36 = 85
    Undefined_37 = 86
    Undefined_38 = 87
    Undefined_39 = 88
    Undefined_40 = 89
    Undefined_41 = 90
    Effects_Level = 91
    Tremulo_Level = 92
    Chorus_Level = 93
    Celeste_Level = 94
    Phaser_Level = 95
    Data_Button_increment = 96
    Data_Button_decrement = 97
    NRPN_LSB = 98
    NRPN_MSB = 99
    RPN_LSB = 100
    RPN_MSB = 101
    Undefined_42 = 102
    Undefined_43 = 103
    Undefined_44 = 104
    Undefined_45 = 105
    Undefined_46 = 106
    Undefined_47 = 107
    Undefined_48 = 108
    Undefined_49 = 109
    Undefined_50 = 110
    Undefined_51 = 111
    Undefined_52 = 112
    Undefined_53 = 113
    Undefined_54 = 114
    Undefined_55 = 115
    Undefined_56 = 116
    Undefined_57 = 117
    Undefined_58 = 118
    Undefined_59 = 119
    All_Sound_Off = (120,Converter.Null)
    Reset_All_Controllers = (121,Converter.Null)
    Local_Control = (122,Converter.OnOff127)
    All_Notes_Off = (123,Converter.Null)
    Omni_Mode_Off = (124,Converter.Null)
    Omni_Mode_On = (125,Converter.Null)
    Mono_Mode_On = 126
    Poly_Mode_On = (127,Converter.Null)
    
    
                
      
class ControlMessage(object):
    
    def __init__(self,data=b''):
        
        command=ControlMessages.make(data[0])
        if command:
            self.command=command
            self.value=command(data[1:])
        else:
            self.command=data[0]
            self.value=data[1]
            
    def __str__(self):
        if self.value is not None:
            return f'{str(self.command)} := {self.value}'
        else:
            return str(self.command)
        
    def __len__(self):
        return 2
          
