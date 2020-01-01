import mido
import pygame

# place-holder until database implemented
# all_mid = ['major-scale.mid']
all_mid = ['RiverFlowsInYou.mid']
# all_mid = ['BohemianRhapsody.mid',
#           'ItsBeginningToLookALotLikeChristmas.mid',
#           'major-scale.mid',
#           'RiverFlowsInYou.mid']


# play the file through the console
def play_with_pygame():  # at the moment unused but keeping as may combine construction file
    pygame.init()
    pygame.mixer.music.load("RiverFlowsInYou.mid")
    length = pygame.time.get_ticks()
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.wait(length)


# check is midi file is type 2 (and removes if so) - this is unlikely but can happen on old sites
def remove_type_2(midi):
    return True if midi.type == 2 else False


# add time from start to message data (for sorting and adjusted delta time purposes)
def add_cumulative_time(msg, current_time):
    add_on = msg.time
    current_time += add_on
    return current_time, add_on


# removes unnecessary meta data types
def filter_meta_type(msg):
    accept = ["set_tempo", "time_signature", "key_signature", "end_of_track"]
    return True if msg.type in accept else False


# removes tempo duplicates and only keeps the last tempo stated for a particular cumulative time
def remove_extra_tempo(msg, msgwithtempos, current_time):
    if (msg.tempo, current_time) not in msgwithtempos[1]:  # only runs following code if new msg isn't a duplicate
        [msgwithtempos.remove(tempo) for tempo in msgwithtempos if tempo == []] # I've added this line out of
        # desperation to try and remove all blank lists but for some reason they are still there fuckk
        # [msgwithtempos.remove(tempo) for tempo in msgwithtempos if tempo[1][1] == current_time] # this is the problem line, i want to be able to run this
        msgwithtempos.append([[msg, current_time], [msg.tempo, current_time]])
        print(msgwithtempos)
        print(msg)
    else:
        pass
    return msgwithtempos


def do_shit(mid, all_messages):  # for each track (then message) do the following
    current_time = 0
    msgwithtempos = [[], []]
    for i, track in enumerate(mid.tracks):
        print(f"Track {i}: {track.name}")
        for msg in track:
            current_time = add_cumulative_time(msg, current_time)[0]
            if msg.type == "sysex data":
                pass
            if msg.is_meta:
                if filter_meta_type(msg):
                    if msg.type == "set_tempo":
                        print(remove_extra_tempo(msg, msgwithtempos, current_time))
                    else:
                        all_messages.append([msg, current_time])
                else:
                    pass
            else:
                all_messages.append([msg, current_time])
    return all_messages

# need to join all_messages list with the second item from the msgwithtempos list


def main():  # for each midi file do the following
    for i in range(0, len(all_mid)):
        all_messages = []
        mid = mido.MidiFile(all_mid[i])
        if remove_type_2(mid):
            i += 1
        else:
            print(do_shit(mid, all_messages))


if __name__ == '__main__':
    main()

