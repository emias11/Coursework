import mido
import pygame
import regulate_tracks

# get the list of midi files from regulate_tracks
list1 = regulate_tracks.main()

# create a blank midi file and add a track to it
mid = mido.MidiFile()
track = mido.MidiTrack()
mid.tracks.append(track)

def get_new_delta_time(delta_time, cumulative_time):
    new_delta_time = cumulative_time - delta_time
    return new_delta_time



# track.append(mido.Message('program_change', program=12, time=0))
# track.append(mido.Message('note_on', note=64, velocity=64, time=32))
# track.append(mido.Message('note_off', note=64, velocity=127, time=32))



def note_to_messages(note, duration):
    x = mido.Message('note_on', note=note, velocity=127,
                 time=0)
    y = mido.Message('note_off', note=note, velocity=0,
                 time=duration)
    return x, y


generated = note_to_messages(57, 577)

bpm = 1000
tempo = mido.midifiles.units.bpm2tempo(bpm)

track.append(mido.MetaMessage('set_tempo', tempo=tempo, time=0))
track.append(generated[0])
track.append(generated[1])
track.append(mido.MetaMessage('end_of_track', time=0))



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


def do_shit(mid):
    for i, track in enumerate(mid.tracks):
        print(f"Track {i}: {track.name}")
        for msg in track:
            print(msg)


do_shit(mid)
