import mido

# all_mid = ['BohemianRhapsody.mid', 'ItsBeginningToLookALotLikeChristmas.mid', 'major-scale.mid', 'RiverFlowsInYou.mid']
all_mid = ['RiverFlowsInYou.mid']


def do_shit(mid):
    print("the type is: " + str(mid.type))
    for i, track in enumerate(mid.tracks):
        print(f"Track {i}: {track.name}")
        for msg in track:
            if msg.is_meta:
                if filter_meta(msg):
                    print(msg)
                else:
                    pass
            else:
                pass

def filter_meta(msg):
    accept = ["set_tempo", "time_signature", "key_signature", "end_of_track"]
    return True if msg.type in accept else False

def main():
    for i in range(0, len(all_mid)):
        mid = mido.MidiFile(all_mid[i])
        do_shit(mid)


main()
# def remove_tempo_duplicates(tempos, times):



"""

 elif not msg.is_meta:
            if msg.type == 'note_on':
                print(msg.note)
for message in track:
                if verbose:
                    print(message)
                if message.type == "set_tempo":
                    self.tempo = message.tempo
                elif message.type == "note_on":
                    if message.time == 0:
                        current_chunk.append(message.note)
                    else:
                        self._sequence(previous_chunk,
                                       current_chunk,
                                       message.time)
                        previous_chunk = current_chunk
                        current_chunk = []

"""