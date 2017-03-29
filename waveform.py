#!/usr/bin/python3

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
    clock wave is specified, such that the output 
