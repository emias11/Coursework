import mido

# all_mid = ['BohemianRhapsody.mid', 'ItsBeginningToLookALotLikeChristmas.mid', 'major-scale.mid', 'RiverFlowsInYou.mid']
# all_mid = ['RiverFlowsInYou.mid']
mid = mido.MidiFile('new_song.mid')

print(mid)


def do_shit(mid):
    for i, track in enumerate(mid.tracks):
        print(f"Track {i}: {track.name}")
        for msg in track:
            print(msg)


do_shit(mid)