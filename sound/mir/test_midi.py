import os
from miditk.smf import MidiFileWriter

# Open file for writing in binary mode.
with open(os.path.join('music', 'minimal.mid'), 'wb') as smf:
    # Create standard MIDI file writer.
    midi = MidiFileWriter(smf)

    # Write file and track header for Type 0 file, one track, 96 pulses per
    # quarter note (ppqn). These are also the default parameter values.
    midi.header(format=0, num_tracks=1, tick_division=96)
    midi.start_of_track()

    # Set tempo to 120 bpm in µsec per quarter note.
    # When no tempo is set in the MIDI file, sequencers will generally assume
    # it to be 120 bpm.
    midi.tempo(int(60000000 / 120))

    # Add MIDI events.
    midi.note_on(channel=0, note=0x40)
    # Advance 192 ticks (i.e. a half note).
    midi.update_ticks(192)
    midi.note_off(channel=0, note=0x40)

    # Add MIDI events.
    midi.note_on(channel=0, note=0x60)
    # Advance 192 ticks (i.e. a half note).
    midi.update_ticks(192)
    midi.note_off(channel=0, note=0x60)

    # End track and midi file.
    midi.end_of_track()
    midi.eof()