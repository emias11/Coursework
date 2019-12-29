import mido
import sys
import pygame

# place-holder until database implemented
# all_mid = ['major-scale.mid']
all_mid = ['RiverFlowsInYou.mid']
# all_mid = ['BohemianRhapsody.mid',
#           'ItsBeginningToLookALotLikeChristmas.mid',
#           'major-scale.mid',
#           'RiverFlowsInYou.mid']


# play the file through the console
def play_with_pygame():
    pygame.init()
    pygame.mixer.music.load("RiverFlowsInYou.mid")
    length = pygame.time.get_ticks()
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.wait(length)


# if midi file type 2, halts program
def remove_type_2(midi):
    print(midi.type)  # remove later
    if midi.type == 2:
        print("invalid file type - does not accept type 2")
        sys.exit()


# add time from start to message data
def add_cumulative_time(msg, current_time):
    add_on = msg.time
    current_time += add_on
    return current_time


# removes unnecessary meta data
def filter_meta(msg):
    accept = ["set_tempo", "time_signature", "key_signature", "end_of_track"]
    if msg.type in accept:
        print(msg)
        valid = True
    else:
        valid = False
        pass
    return valid


def do_shit(mid):
    current_time = 0
    remove_type_2(mid)
    for i, track in enumerate(mid.tracks):
        print(f"Track {i}: {track.name}")
        for msg in track:
            current_time = add_cumulative_time(msg, current_time)
            if msg.type == "sysex data":
                ...
            if msg.is_meta:
                if filter_meta(msg):
                    print(current_time)
                else:
                    pass
            else:
                print(msg)
                print(current_time)


def main():
    for i in range(0, len(all_mid)):
        mid = mido.MidiFile(all_mid[i])
        do_shit(mid)


main()

