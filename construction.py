import mido
import pygame
import regulate_tracks
import Markov
import time


def note_to_messages(note, current_time, duration, velocity_on, velocity_off, note_message_list, channel):
    x = mido.Message('note_on', channel=channel, note=note, velocity=velocity_on, time=0)
    y = mido.Message('note_off', channel=channel, note=note, velocity=velocity_off, time=0)
    note_message_list.append([x, current_time])
    note_message_list.append([y, current_time+duration])


def generate_note_on_offs(list_of_lists, track):
    current_time = 0
    note_message_list = []
    new_pitch = list_of_lists[0]
    new_note_lengths = list_of_lists[1]
    new_delays = list_of_lists[2]
    new_velocity_on = list_of_lists[3]
    new_velocity_off = list_of_lists[4]
    for i in range(500):
        note_to_messages(new_pitch[i], current_time, new_note_lengths[i], new_velocity_on[i],
                         new_velocity_off[i], note_message_list, 2)
            # THIS IS A PLACEHOLDER VALUE FOR CHANNEL
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
    # above sorts by second element of list which is time
    running_time = 0
    for item in sorted_note_message_list:
        msg = item[0]
        msg.time = item[1] - running_time
        running_time += (item[1] - running_time)
        track.append(msg)


def play_with_pygame(song):
    pygame.init()
    pygame.mixer.music.load(song)
    length = pygame.time.get_ticks()
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.wait(length)


def put_together_song(track, channels_list_dict, list1):
    # PLACEHOLDER VALUESSSSS FOR PROGRAM
    for item in list1:
        msg = item[0]
        if msg.type == 'program_change':
            msg.time = 0
            track.append(mido.Message('program_change', channel=msg.channel, program=msg.program, time=0))

    note_message_list = generate_note_on_offs(channels_list_dict[26], track)
    # note_message_list is an ordered list of just msgs (no cumulative time) and their appropriate delta times
    print(note_message_list)
    append_notes(note_message_list, track)


def main():
    output, ticksperbeat = regulate_tracks.main()  # input songs as parameters here?
    list1 = output
    channels_list_dict = Markov.main()
    mid = mido.MidiFile()
    track = mido.MidiTrack()
    mid.tracks.append(track)
    mid.ticks_per_beat = ticksperbeat
    track.ticks_per_beat = ticksperbeat

    put_together_song(track, channels_list_dict, list1)

    mid.save('new_song.mid')
    play_with_pygame('new_song.mid')


if __name__ == '__main__':
    main()


