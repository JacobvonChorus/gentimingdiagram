#!/usr/bin/python3

# Represents a set of waveforms in a timing diagram.
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


class Wave:
    """Wave is used to represent a single waveform in a diagram.

    A wave has a text label, and a sequence of high and low ticks which
    correspond to the output."""

    def __init__(self, label, ticks):
        """Creates a single wave object representing a waveform.

        Constructs a representation of a waveform.

        Args:
            label: Name of signal displayed in output
            ticks: The high and low values of the waveform for each tick (half
                a clock period.
        """
        self.label = label
        self.ticks = ticks

class TimingDiagram:
    """An array of waveforms

    Stores a series of Wave objects to be displayed together in the output. The
    clock wave and active edge are specififed, such that the output can be
    formatted accordingly.
    """

    def __init__(self):
        """Initialize an empty timing diagram"""
        self.clk_index = -1 # Can only be set once per instance
        self.wave_list = []
        self.rising_edge = 1 # 1: rising, 0: falling

    def addWave(self, wave, isclk):
        """Add waveform to timing diagram.

        Args:
            wave: Wave object to be added
            isclk: 1 if this is to be a clock, zero otherwise. Can only be set
                once per object instance
        """
        if self.clk_index >= 0 and isclk:
            raise Exception('Can only set CLK once per timing diagram.')
        self.wave_list.append(wave)
        if isclk:
            self.clk_index = len(self.wave_list)

    def setRisingFalling(self, isrising):
        """Set if active clock edge is rising or falling.

        isrising: 1 -> rising, 0 -> falling
        """
        if isrising:
            self.rising_edge = 1
        else:
            self.rising_edge = 0


