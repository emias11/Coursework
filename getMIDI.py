import mido

midi = mido.MidiFile("C:/Users/stapl/OneDrive/Documents/Documents/Coursework/AUD_HTX0085.mid")
midi.ticks_per_beat = midi.ticks_per_beat
previous_chunk = []
current_chunk = []

def sequence(midi):
    for track in midi.tracks:

        def inspect(filename):
            mid = mido.MidiFile(filename)
            for i, track in enumerate(mid.tracks):
                print('Track {}: {}'.format(i, track.name))
                for message in track:
                    print(message)

'''
for track in midi.tracks:
    for message in track:
        # if verbose:
        #   print(message)
        if message.type == "set_tempo":
            midi.tempo = message.tempo
        elif message.type == "note_on":
            if message.time == 0:
                current_chunk.append(message.note)
            else:
                sequence(previous_chunk,
                               current_chunk,
                               message.time)
                previous_chunk = current_chunk
                current_chunk = []

def inspect(filename):
    mid = mido.MidiFile(filename)
    for i, track in enumerate(mid.tracks):
        print('Track {}: {}'.format(i, track.name))
        for message in track:
            print(message)


inspect('AUD_HTX0085')
'''

"""
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
"""