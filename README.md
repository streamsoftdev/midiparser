# MIDI Parser

Adapted from `MIDIFile` provided by Julian Porter under the MIT License, [https://pypi.org/project/MIDIFile/], [julian@porternet.org]. No license notice was provided with the downloadable source code and so it is not replicated here. The original author information has been retained in each source file.

Derivative work, licensed under the Apache License version 2.0. 

## Main changes

Included support for correctly parsing running status MIDI messages (without which the parsing is incorrect for most MIDI files), and included a much greater range of control message types, and other event parsing.

## Minor changes

Changes to way some parsed values are represented, and some minor bug fixes.



