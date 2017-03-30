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

def __startSVG(timingdiagram, fsvg):
    """Determine necessary file sizes and start file"""
    fsvg.write('<?xml version="1.0" encoding="UTF-8" ?>\n')

def __stopSVG(filename, fsvg):
    """Finish and output file"""
    fsvg.write('</svg>\n')

def timingDiagramToSVG(timingdiagram, filename):
    """Outputs a TimingDiagram object to an svg file."""
    fsvg = open(filename, 'w')
    __startSVG(timingdiagram, fsvg)
    __stopSVG(filename, fsvg)
    fsvg.close()

timingDiagramToSVG(0, 'output.svg')
