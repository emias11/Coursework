import mido
import pygame

# place-holder until database implemented
# all_mid = ['major-scale.mid']
# all_mid = ['RiverFlowsInYou.mid']
# all_mid = ['BohemianRhapsody.mid']


all_mid = ['BohemianRhapsody.mid',
           'ItsBeginningToLookALotLikeChristmas.mid',
           'major-scale.mid',
           'RiverFlowsInYou.mid']


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
    if not msgwithtempos:  # if the list is empty
        msgwithtempos.append([msg, current_time])
    else:
        for i in range(len(msgwithtempos)):
            msgwithtempo = msgwithtempos[i]
            if msgwithtempo[1] == current_time:  # this checks duplicates
                msgwithtempos.remove(msgwithtempo)
        msgwithtempos.append([msg, current_time])
    return msgwithtempos


def sort(list_of_lists):
    low = 0
    high = len(list_of_lists) - 1
    quick_sort(list_of_lists, low, high)
    return list_of_lists


def partition(alist, low, high):
    i = (low - 1)
    pivot = alist[high][1]
    for j in range(low, high):
        if alist[j][1] <= pivot:
            i += 1
            alist[i], alist[j] = alist[j], alist[i]
    alist[i + 1], alist[high] = alist[high], alist[i + 1]
    return i + 1


def quick_sort(alist, low, high):
    if low < high:
        pi = partition(alist, low, high)
        quick_sort(alist, low, pi - 1)
        quick_sort(alist, pi + 1, high)


def do_shit(mid, all_messages):  # for each track (then message) do the following
    msgwithtempos = []
    for i, track in enumerate(mid.tracks):
        current_time = 0
        # print(f"Track {i}: {track.name}")
        for msg in track:
            current_time = add_cumulative_time(msg, current_time)[0]
            if msg.type == "sysex data":
                pass
            elif msg.is_meta:
                if filter_meta_type(msg):
                    if msg.type == "set_tempo":
                        msgwithtempos = remove_extra_tempo(msg, msgwithtempos, current_time)
                    else:
                        all_messages.append([msg, current_time])
            else:
                all_messages.append([msg, current_time])
    return all_messages, msgwithtempos


def main():  # for each midi file do the following
    all_lists = []
    for i in range(0, len(all_mid)):
        all_messages = []
        mid = mido.MidiFile(all_mid[i])
        print(mid.type)
        if not remove_type_2(mid):
            all_messages, msgwithtempos = do_shit(mid, all_messages)
            final_messages = all_messages + msgwithtempos
            final_messages = sort(final_messages)
            all_lists.append(final_messages)
    print(all_lists)
    return all_lists


if __name__ == '__main__':
    main()