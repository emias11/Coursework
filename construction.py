import mido
import pygame
import regulate_tracks
import Markov


def note_to_messages(note, current_time, duration, velocity_on, velocity_off, track):
    x = mido.Message('note_on', note=note, velocity=velocity_on, time=current_time)
    y = mido.Message('note_off', note=note, velocity=velocity_off, time=(current_time+duration))
    #track.append(x)
    #track.append(y)
    #return x, y


def generate_note_on_offs(list_of_lists, track):
    current_time = 0
    song_note_length = list_of_lists[0]
    new_pitch = list_of_lists[1]
    new_note_lengths = list_of_lists[2]
    new_delays = list_of_lists[3]
    new_velocity_on = list_of_lists[4]
    new_velocity_off = list_of_lists[5]
    for i in range(song_note_length):
        note_to_messages(new_pitch[i], current_time, new_note_lengths[i], new_velocity_on[i], new_velocity_off[i], track)
        try:
            current_time += new_delays[i]
            print(new_delays[i])
        except IndexError:
            current_time += 0


def play_with_pygame(song):
    pygame.init()
    pygame.mixer.music.load(song)
    length = pygame.time.get_ticks()
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.wait(length)


def main():
    output, ticksperbeat = regulate_tracks.main()
    list1 = output
    channels_list_dict = Markov.main()

    mid = mido.MidiFile()
    track = mido.MidiTrack()
    mid.tracks.append(track)
    mid.ticks_per_beat = ticksperbeat
    track.ticks_per_beat = ticksperbeat

    generate_note_on_offs(channels_list_dict[26], track)
    #generate_note_on_offs(channels_list_dict[32], track)

    mid.save('new_song.mid')
    play_with_pygame('new_song.mid')


if __name__ == '__main__':
    main()

"""
def get_new_delta_time(delta_time, cumulative_time):
    new_delta_time = cumulative_time - delta_time
    return new_delta_time
"""

"""
generated = note_to_messages(57, 800)

bpm = 1000
tempo = mido.midifiles.units.bpm2tempo(bpm)

track.append(mido.MetaMessage('set_tempo', tempo=tempo, time=0))
track.append(generated[0])
track.append(generated[1])
track.append(mido.MetaMessage('end_of_track', time=0))
"""


# track.append(mido.Message(message0))
#track.append(mido.Message(message1))
#track.append(mido.Message(message2))
# track.append(mido.Message(message3))

