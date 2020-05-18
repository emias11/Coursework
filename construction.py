import mido
import pygame
import regulate_tracks
from probabilities import get_channels_dict
from Markov import get_song_inputs, get_lists_for_all_channels


def note_to_messages(note, current_time, duration, velocity_on, velocity_off, note_message_list, channel):
    x = mido.Message('note_on', channel=channel, note=note, velocity=velocity_on, time=0)
    y = mido.Message('note_off', channel=channel, note=note, velocity=velocity_off, time=0)
    note_message_list.append([x, current_time])
    note_message_list.append([y, current_time+duration])


def generate_note_on_offs(list_of_lists, channel):
    current_time = 0
    note_message_list = []
    new_pitch = list_of_lists[0]
    new_note_lengths = list_of_lists[1]
    new_delays = list_of_lists[2]
    new_velocity_on = list_of_lists[3]
    new_velocity_off = list_of_lists[4]
    """
    print(channel)
    for delay in new_delays:
        if delay < 0:
            print(delay)
    print()
    """
    for i in range(500):
        note_to_messages(new_pitch[i], current_time, new_note_lengths[i], new_velocity_on[i],
                         new_velocity_off[i], note_message_list, channel)
        try:
            current_time += new_delays[i]
        except IndexError:
            current_time += 0
    return note_message_list


def append_notes(note_message_list, track):
    # for all messages, index the list backwards then take the last instance.
    # With one instrument should just be all the notes
    # maybe add dummy messages to test before u get variables passing
    sorted_note_message_list = sorted(note_message_list, key=lambda x: x[1])
    # above sorts by second element of list which is (CUMULATIVE?) time
    running_time = 0
    for item in sorted_note_message_list:
        msg = item[0]
        time = item[1] - running_time
        msg.time = abs(time)
        running_time += time
        track.append(msg)


def play_with_pygame(song):
    pygame.init()
    pygame.mixer.music.load(song)
    length = pygame.time.get_ticks()
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.wait(length)


def put_together_song(track, channels_lists_dict, list1, channels, programs, channels_dict):
    for item in list1:
        msg = item[0]
        if msg.type == 'program_change':
            msg.time = 0
            track.append(mido.Message('program_change', channel=msg.channel, program=msg.program, time=0))

    extended_list_of_msgs = []
    for program in programs:
        note_message_list = generate_note_on_offs(channels_lists_dict[int(program)], channels_dict[int(program)])
        # note_message_list is an ordered list of just msgs (no cumulative time) and their appropriate delta times
        for item in note_message_list:
            extended_list_of_msgs.append(item)

    append_notes(extended_list_of_msgs, track)


def main():
    output, ticksperbeat = regulate_tracks.main()  # input songs as parameters here?
    list1 = output
    channels_dict = get_channels_dict(list1)

    mid = mido.MidiFile()
    track = mido.MidiTrack()
    mid.tracks.append(track)
    mid.ticks_per_beat = ticksperbeat
    track.ticks_per_beat = ticksperbeat

    # functions from Markov.py
    channels, programs = get_song_inputs(list1)
    channels_lists_dict = get_lists_for_all_channels(channels, list1)
    # creates dict where {program: [list of lists for sequences of each parameter}

    put_together_song(track, channels_lists_dict, list1, channels, programs, channels_dict)

    mid.save('new_song.mid')
    play_with_pygame('new_song.mid')


if __name__ == '__main__':
    main()


