#!/usr/bin/python3

# Reads the plain text timing diagram and constructs the necessary objects.
# Copyright © 2017 Jacob von Chorus <jacobvonchorus@cwphoto.ca>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import waveform
import wavetosvg

timingDiagram = waveform.TimingDiagram()


def parseWaveLine(timingLine):
    global timingDiagram
    label = timingLine.split()[0]
    ticks = timingLine.split('$')[1].rstrip('\n')
    newWaveform = waveform.Wave(label, ticks)
    timingDiagram.addWave(newWaveform, label == 'CLK')



# expects: binary name, input file, output
if len(sys.argv) != 3:
    print('usage: gentiming.py timingdata svg\n' +
            '\t timingdata: plain text waveform input\n' +
            '\t svg: output SVG image')
    sys.exit(1)
inputfile = sys.argv[1]
outputsvg = sys.argv[2]

# Create TimingDiagram from file, the object is a global variable
with open(inputfile, 'r') as ftiming:
    isfirst = True # First line contains config
    for timingLine in ftiming:
        if isfirst: # Parse config
            isfirst = False
            wavetosvg.parseConfigLine(timingLine)
        else:
            if not timingLine[0].isalnum():
                pass # Ignore blank lines
            else:
                parseWaveLine(timingLine)

wavetosvg.timingDiagramToSVG(timingDiagram, outputsvg)
