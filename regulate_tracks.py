import mido
import pygame


# place-holder until database implemented
# all_mid = ['major-scale.mid']
# all_mid = ['Gloria-Mozart.MID.mid']
# all_mid = ['BohemianRhapsody.mid']
# all_mid = ['ItsBeginningToLookALotLikeChristmas.mid']
all_mid = [' (Yiruma).mid']
# all_mid = ['BohemianRhapsody.mid']


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
    accept = ["set_tempo"]  # kept key signature and time signature, actually don't need it
    return True if msg.type in accept else False


# removes tempo duplicates and only keeps the last tempo stated for a particular cumulative time
def remove_extra_tempo(msg, msgwithtempos, current_time):
    if not msgwithtempos:  # if the list is empty
        msgwithtempos.append([msg, current_time])
    else:
        for i in range(len(msgwithtempos)):
            msgwithtempo = msgwithtempos[i]
            if msgwithtempo[1] == current_time:  # this checks duplicates
                msgwithtempos.remove(msgwithtempo)
        msgwithtempos.append([msg, current_time])
    return msgwithtempos


def do_shit(mid, all_messages):  # for each track (then message) do the following
    msgwithtempos = []
    for i, track in enumerate(mid.tracks):
        current_time = 0
        # print(f"Track {i}: {track.name}")
        for msg in track:
            current_time = add_cumulative_time(msg, current_time)[0]
            # if msg.type == "control_change":
                # pass
            # talk about this as an error as thought not important but important
            if msg.type == "sysex data":  # this doesn't seem to do anything , probably doesn't matter
                pass
            elif msg.is_meta:
                if msg.type == "set_tempo":
                    msgwithtempos = remove_extra_tempo(msg, msgwithtempos, current_time)
                else:
                    pass
            else:
                all_messages.append([msg, current_time])
    return all_messages, msgwithtempos


def main():  # for each midi file do the following
    all_lists = []
    for i in range(0, len(all_mid)):
        all_messages = []
        mid = mido.MidiFile(all_mid[i])
        ticksperbeat = mid.ticks_per_beat
        if not remove_type_2(mid):
            all_messages, msgwithtempos = do_shit(mid, all_messages)
            final_messages = all_messages + msgwithtempos
            final_messages = sorted(final_messages, key=lambda x: x[1])
            all_lists += final_messages
    for i, item in enumerate(all_lists):
        if all_lists[i][0].type == "set_tempo":
            while all_lists[i+1][0].type == "set_tempo": #talk about this as an error with i-1 being logical but not working
                all_lists.pop(i+1)
    for i in all_lists:
        print(i)
    return all_lists, ticksperbeat


if __name__ == '__main__':
    main()
