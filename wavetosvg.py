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

vertLines = False # default no lines on clock
activeEdge = 1 # 1 = rising, 0 = falling
showArrow = False
italicCLK = False # print clk label in italics

maxlabel = 0 # stored to right justify labels
svgWidth = 0
svgHeight = 0


def __startSVG(timingDiagram, fsvg):
    """Determine necessary file sizes and start file"""
    global maxlabel
    global svgWidth
    global svgHeight
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
    if wave.label == 'CLK' and italicCLK:
        fontStyle = ' font-style="italic"'
    else:
        fontStyle = ''
    fsvg.write('\t<text x="{}" y="{}" font-family="monospace"{}>{}</text>\n'.format(
        (maxlabel - len(wave.label))*charWidth, y, fontStyle, wave.label))

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


def __printVertLines(fsvg, clk):
    for i,tick in enumerate(clk):
        if i == 0: # no vert line at the beginning
            continue
        # Using configured active edge, check if that's the case
        if ((activeEdge and tick == '-' and clk[i - 1] == '_') or
                (not activeEdge and tick == '_' and clk[i - 1] == '-')):
            x = (maxlabel * charWidth) + spacing + (i * tickWidth)
            y1 = spacing
            y2 = svgHeight - spacing
            fsvg.write('\t<line x1="{}" y1="{}" x2="{}" y2="{}" '
                    .format(x, y1, x, y2) +
                    'stroke-dasharray="4,2" stroke="darkslategrey" ' +
                    'stroke-width=".3" />\n')

def __printClkArrows(fsvg, clk, clkIndex):
    for i,tick in enumerate(clk):
        if i == 0:
            continue
        x = (maxlabel * charWidth) + spacing + (i * tickWidth)
        # middle of clk line
        y = spacing + clkIndex * (spacing + lineHeight) + (lineHeight / 2)
        arrowLeft = x - tickWidth / 10
        arrowRight = x + tickWidth / 10

        # rising edge case
        if activeEdge and tick == '-' and clk[i - 1] == '_':
            arrowTop = y - lineHeight / 10
            arrowBottom = y + lineHeight / 10
            fsvg.write('\t<polygon points="{},{} {},{} {},{}" '
                    .format(x, arrowTop, arrowLeft, arrowBottom,
                        arrowRight, arrowBottom) +
                    'style="fill:black;stroke:blacka />\n"')
        if not activeEdge and tick == '_' and clk[i - 1] == '-':
            arrowTop = y - lineHeight / 10
            arrowBottom = y + lineHeight / 10
            fsvg.write('\t<polygon points="{},{} {},{} {},{}" '
                    .format(x, arrowBottom, arrowLeft, arrowTop,
                        arrowRight, arrowTop) +
                    'style="fill:black;stroke:blacka />\n"')


def __stopSVG(filename, fsvg):
    """Finish and output file"""
    fsvg.write('</svg>\n')



def parseConfigLine(configLine):
    global vertLines
    global activeEdge
    global showArrow
    global italicCLK
    for configDirty in configLine.split(','):
        config = configDirty.strip() # dirty until whitespace removed
        if config == 'SHOW_VERT':
            vertLines = True
        elif config == 'FALLING_EDGE':
            activeEdge = 0
        elif config == 'SHOW_ARROW':
            showArrow = True
        elif config == 'ITALIC_CLK':
            italicCLK = True


def timingDiagramToSVG(timingdiagram, filename):
    """Outputs a TimingDiagram object to an svg file."""
    if not activeEdge: # if falling edge was requrested, set it
        timingdiagram.setRisingFalling(0)

    fsvg = open(filename, 'w')
    __startSVG(timingdiagram, fsvg)

    # vertLines rendered first if any
    if vertLines and timingdiagram.clk_index != -1:
        __printVertLines(fsvg,
                timingdiagram.wave_list[timingdiagram.clk_index].ticks)
    # print waveforms
    for i,wave in enumerate(timingdiagram.wave_list):
        #one blank line between lines, a 'spacing' at top
        __printWave(fsvg, wave, i * (spacing + lineHeight) + lineHeight + spacing)
    # show arrowheads if requested
    if showArrow and timingdiagram.clk_index != -1:
        __printClkArrows(fsvg,
                timingdiagram.wave_list[timingdiagram.clk_index].ticks,
                timingdiagram.clk_index)

    __stopSVG(filename, fsvg)
    fsvg.close()

