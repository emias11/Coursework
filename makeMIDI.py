from midiutil import MIDIFile

degrees = [60, 62, 64, 65, 67, 69, 71, 72]  # MIDI note number
track = 0
channel = 0
time = 0  # In beats
time2 = 4
# new stuff
program = 123  # subtract one from docs as this is indexed from 0 
duration = 10   # In beats
# tempo = 120  # In BPM
volume = 100  # 0-127, as per the MIDI standard

MyMIDI = MIDIFile(1)  # One track, defaults to format 1 (tempo track automatically created)
MyMIDI.addTempo(track, 4, 120)
MyMIDI.addProgramChange(track, channel, time2, program)

for pitch in degrees:
    MyMIDI.addNote(track, channel, pitch, time, duration, volume)
    time = time + 1

with open("major-scale.mid", "wb") as output_file:
    MyMIDI.writeFile(output_file)

