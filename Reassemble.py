import mido

mid = mido.MidiFile('RiverFlowsInYou.mid')

for i, track in enumerate(mid.tracks):
    print(f"Track {i}: {track.name}")
    for msg in track:
        if msg.is_meta:
            pass
        else:
            print(msg.type, msg.channel, msg.time)
            if msg.type == 'note_on' or msg.type == 'note_off':
                print(msg.type)
                print(msg.note)
            elif msg.type == 'program_change':
                pass
            # elif msg.type == 'control_change':









def cumulative_time(last_time, add_on):
    last_time += add_on
    return last_time
