import mido
import pygame


def play_with_pygame(song):
    pygame.init()
    pygame.mixer.music.load(song)
    length = pygame.time.get_ticks()
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.wait(length)


mid = mido.MidiFile()
track = mido.MidiTrack()
mid.tracks.append(track)

# channel = [0, 1, 2, 3, 4, 5, 6, 7]
# note = [60, 62, 64, 65, 67, 69, 71, 72]


track.append(mido.Message('program_change', channel=0, program=127, time=0))
track.append(mido.Message('note_on', channel=0, note=60, velocity=100, time=0))

track.append(mido.Message('note_on', channel=0, note=62, velocity=100, time=960))

track.append(mido.Message('note_on', channel=0, note=64, velocity=100, time=960))

track.append(mido.Message('note_on', channel=0, note=65, velocity=100, time=960))

track.append(mido.Message('note_on', channel=0, note=67, velocity=100, time=960))

track.append(mido.Message('note_on', channel=0, note=69, velocity=100, time=960))

track.append(mido.Message('note_on', channel=0, note=71, velocity=100, time=960))

track.append(mido.Message('note_on', channel=0, note=72, velocity=100, time=960))

track.append(mido.Message('note_off', channel=0, note=60, velocity=100, time=960))

track.append(mido.Message('note_off', channel=0, note=62, velocity=100, time=960))

track.append(mido.Message('note_off', channel=0, note=64, velocity=100, time=960))

track.append(mido.Message('note_off', channel=0, note=65, velocity=100, time=960))

track.append(mido.Message('note_off', channel=0, note=67, velocity=100, time=960))

track.append(mido.Message('note_off', channel=0, note=69, velocity=100, time=960))

track.append(mido.Message('note_off', channel=0, note=71, velocity=100, time=960))

track.append(mido.Message('note_off', channel=0, note=72, velocity=100, time=960))
track.append(mido.MetaMessage('end_of_track', time=0))


mid.save('pianoscale.mid')

play_with_pygame('pianoscale.mid')