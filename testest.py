import mido
import pygame

oldmid = mido.MidiFile('major-scale.mid')


def play_with_pygame(song):
    pygame.init()
    pygame.mixer.music.load(song)
    length = pygame.time.get_ticks()
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.wait(length)

def get_list(mid):
    lst = []
    for i, track in enumerate(oldmid.tracks):
        print(f"Track {i}: {track.name}")
        for msg in track:
            lst.append(msg)
    return lst


def main():
    mid = mido.MidiFile()
    track = mido.MidiTrack()
    mid.tracks.append(track)
    lst = get_list(oldmid)
    for i in range(0, len(lst)):
        new_message = lst[i]
        track.append(new_message)
    mid.save('new_song.mid')

    play_with_pygame('new_song.mid')


if __name__ == '__main__':
    main()
