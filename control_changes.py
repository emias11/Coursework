import mido

mid = mido.MidiFile('ItsBeginningToLookALotLikeChristmas.mid')

for i, track in enumerate(mid.tracks):
    print(f"Track {i}: {track.name}")
    for msg in track:
        if msg.type == 'control_change':
            print(msg)
        else:
            pass
