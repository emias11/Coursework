import mido
import pygame
import regulate_tracks
from Markov import get_lists_for_all_channels


# create a blank midi file and add a track to it
mid = mido.MidiFile()
track = mido.MidiTrack()
mid.tracks.append(track)


def note_to_messages(note, duration, velocity_on, velocity_off):
    x = mido.Message('note_on', note=note, velocity=127,
                 time=0)
    y = mido.Message('note_off', note=note, velocity=0,
                 time=duration)
    return x, y


def generate_note_on_offs(song_note_length, new_pitch, new_note_lengths, new_delays, new_velocity_on, new_velocity_off):
    for i in range(len(song_note_length)):
        print(new_pitch)
        # note_to_messages('note_on', note=new_pitch[i],  )

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
mid.save('new_song.mid')
print(mid)


def play_with_pygame(song):
    pygame.init()
    pygame.mixer.music.load(song)
    length = pygame.time.get_ticks()
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.wait(length)


play_with_pygame('new_song.mid')


def main():
    output, ticksperbeat = regulate_tracks.main()
    list1 = output
    song_note_length, new_pitch, new_note_lengths, new_delays, new_velocity_on, new_velocity_off = make_lists_for_all_parameters(list1)
    generate_note_on_offs(song_note_length, new_pitch, new_note_lengths, new_delays, new_velocity_on, new_velocity_off)


if __name__ == '__main__':
    main()

"""
def get_new_delta_time(delta_time, cumulative_time):
    new_delta_time = cumulative_time - delta_time
    return new_delta_time
"""


