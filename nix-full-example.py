#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, division

import numpy as np
from nix import *

f = File.open("full-example.h5", FileMode.Overwrite)

rec01 = f.create_block("Session 01", "recordingsession")

# sources
tet = rec01.create_source("Tetrode 01", "tetrode")
chans = list()
for i in range(4):
    chans.append(tet.create_source("Channel 0" + str(i + 1), "recordingchannel"))

# simple signals
delta = 0.1
data = np.sin(np.arange(0, 10, delta)) * 10 - 60
sigs = list()
for i in range(4):
    sig = rec01.create_data_array("Signal 0" + str(i + 1), "analogsignal", DataType.Double, (len(data), ))
    sig.data[:] = data
    sig.label = "Voltage"
    sig.unit  = "mV"
    sig.sources.append(chans[i])

    dim = sig.append_sampled_dimension(delta)
    dim.label = "Time"
    dim.unit  = "s"
    sigs.append(sig)

# stimulus
stim = rec01.create_data_array("Stimulus", "stimulus", DataType.Double, (len(data), ))

# spiketrains
spikes = list()
for i in range(4):
    st = rec01.create_data_array("Spikes 0" + str(i + 1), "spiketrain", DataType.Double, (10, ))
    st.data[:] = np.arange(0, 10)
    st.unit  = 's'
    st.label = 'time'
    st.append_set_dimension()
    spikes.append(st)

# tags for spikes
mtags = list()
for i in range(4):
    mt = rec01.create_multi_tag("Tagged Spikes 0" + str(i + 1), "spiketrain", spikes[i])
    mt.references.append(sigs[i])
    mtags.append(mt)

# tag for the whole trial
tag = rec01.create_tag("Trial 01", "trial", (0.0, ))
tag.extent = (10, )
feature = tag.create_feature(stim, LinkType.Tagged)
for sig in sigs:
    tag.references.append(sig)
for st in spikes:
    tag.references.append(st)

# metadata for session
rec_sec = f.create_section("Session 01", "recordingsession")
rec_sec.create_property("Experimenter", (Value("Thomas Wachtler"), ))
rec01.metadata = rec_sec

tet_sec = rec_sec.create_section("Tetrode 01", "tetrode")
tet_sec.create_property("Manufacturer", (Value("Thomas Recordings"), ))
tet_sec.create_property("ElectrodeCount", (Value(4), ))
tet.metadata = tet_sec

sub_sec = rec_sec.create_section("Subject 01", "subject")
sub_sec.create_property("Species", (Value("Macaca mulatta"), ))
sub_sec.create_property("Name", (Value("Maoli"), ))
sub_sec.create_property("Age", (Value(6), ))



f.close()