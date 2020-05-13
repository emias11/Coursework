import mido
import pygame


# place-holder until database implemented
# all_mid = ['major-scale.mid']
# all_mid = ['Gloria-Mozart.MID.mid']
# all_mid = ['BohemianRhapsody.mid']
all_mid = ['ItsBeginningToLookALotLikeChristmas.mid', 'BohemianRhapsody.mid']
# all_mid = [' (Yiruma).mid']


# check is midi file is type 2 (and removes if so) - this is unlikely but can happen on old sites
def remove_type_2(midi):
    return True if midi.type == 2 else False


# add time from start to message data (for sorting and adjusted delta time purposes)
def add_cumulative_time(msg, current_time):
    add_on = msg.time
    current_time += add_on
    return current_time, add_on

"""
# removes tempo duplicates and only keeps the last tempo stated for a particular cumulative time
def remove_extra_tempo(msg, msgwithtempos, current_time):
    if not msgwithtempos:  # if the list is empty
        msgwithtempos.append([msg, current_time])  # append the tempo message along with the cumulative time
    else:
        for i in range(len(msgwithtempos)):  # iterate through the current list of tempo messages + cumulative_times
            msgwithtempo = msgwithtempos[i]  # allocate to the variable msgwithtempo the i item in the list
            if msgwithtempo[1] == current_time:  # this checks for cumulative time duplicates
                msgwithtempos.remove(msgwithtempo)  # removes from the list if duplicate (if found)
        msgwithtempos.append([msg, current_time])  # adds the new tempo to the list (with its cumulative time)
    return msgwithtempos
"""


def do_shit(mid, all_messages):  # for each track (then message) do the following
    msgwithtempos = []
    for i, track in enumerate(mid.tracks):
        current_time = 0
        # print(f"Track {i}: {track.name}")
        for msg in track:
            current_time = add_cumulative_time(msg, current_time)[0]
            allowed_types = ["note_on", "note_off", "program_change", "set_tempo"]  # can add control_changes
            if msg.type in allowed_types:
                all_messages.append([msg, current_time])
            # elif msg.type == "set_tempo":
                # all_messages.append([msg, current_time])
                # msgwithtempos = remove_extra_tempo(msg, msgwithtempos, current_time)
            else:
                pass
            # else:
                # all_messages.append([msg, current_time])
    return all_messages, msgwithtempos


def main():  # for each midi file do the following
    all_lists = []
    ticksperbeat = 0
    for i in range(0, len(all_mid)):
        all_messages = []
        mid = mido.MidiFile(all_mid[i])
        ticksperbeat += mid.ticks_per_beat  # change this to be average ticks per beat
        if not remove_type_2(mid):
            all_messages, msgwithtempos = do_shit(mid, all_messages)
            final_messages = all_messages + msgwithtempos
            final_messages = sorted(final_messages, key=lambda x: x[1])
            all_lists += final_messages
    ticksperbeat = ticksperbeat//len(all_mid)
    for i, item in enumerate(all_lists):
        # this gets rid of excess set_tempo messages
        if all_lists[i][0].type == "set_tempo":
            while all_lists[i+1][0].type == "set_tempo":  # talk about trying this with i and i-1?
                all_lists.pop(i)
    return all_lists, ticksperbeat


if __name__ == '__main__':
    main()


