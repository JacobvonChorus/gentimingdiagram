#!/usr/bin/python3

# Translates a timing diagram object to an SVG.
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

import waveform

textHeight = 10
charWidth = 7.5
lineHeight = 20
tickWidth = 20
spacing = 10

maxlabel = 0 # stored to right justify labels

def __startSVG(timingDiagram, fsvg):
    """Determine necessary file sizes and start file"""
    global maxlabel
    maxlabel = max(len(wave.label) for wave in timingDiagram.wave_list)
    maxticks = max(len(wave.ticks) for wave in timingDiagram.wave_list)
    labelWidth = maxlabel * charWidth
    waveWidth = maxticks * tickWidth
    svgWidth = labelWidth + waveWidth + 2*spacing # one space at end of waves
    svgHeight = len(timingDiagram.wave_list) * (spacing + lineHeight) + spacing

    fsvg.write('<?xml version="1.0" encoding="UTF-8" ?>\n')
    fsvg.write('<svg width="{}" height="{}" xmlns="http://www.w3.org/2000/svg"'
            ' version="1.1">\n'.format(svgWidth, svgHeight))

def __printWave(fsvg, wave, y):
    fsvg.write('\t<text x="{}" y="{}" font-family="monospace">{}</text>\n'.format(
        (maxlabel - len(wave.label))*charWidth, y, wave.label))
    for i,tick in enumerate(wave.ticks):
        x = (maxlabel * charWidth) + spacing + (i * tickWidth)
        # tick is at bottom, or top
        if tick == '-':
            yprime = y - lineHeight
        else:
            yprime = y
        fsvg.write('\t<line x1="{}" y1="{}" x2="{}" y2="{}" stroke="black" />\n'
                .format(x, yprime, x + tickWidth, yprime))
        # if transition tick, draw vertical line
        if (i != 0) and (tick != wave.ticks[i - 1]):
            fsvg.write('\t<line x1="{}" y1="{}" x2="{}" y2="{}" stroke="black"/>\n'
                    .format(x, y, x, y - lineHeight))

def __stopSVG(filename, fsvg):
    """Finish and output file"""
    fsvg.write('</svg>\n')

def timingDiagramToSVG(timingdiagram, filename):
    """Outputs a TimingDiagram object to an svg file."""
    fsvg = open(filename, 'w')
    __startSVG(timingdiagram, fsvg)
    for i,wave in enumerate(timingdiagram.wave_list):
        #one blank line between lines, a 'spacing' at top
        __printWave(fsvg, wave, i * (spacing + lineHeight) + lineHeight + spacing)
    __stopSVG(filename, fsvg)
    fsvg.close()

