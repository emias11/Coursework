import mido
import pygame
import regulate_tracks


def play_with_pygame(song):
    pygame.init()
    pygame.mixer.music.load(song)
    length = pygame.time.get_ticks()
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.wait(length)


def printmessages(mid):
    for i, track in enumerate(mid.tracks):
        print(f"Track {i}: {track.name}")
        for msg in track:
            print(msg)


def main():
    # get the list of midi files from regulate_tracks
    list1 = regulate_tracks.main()

    # create a blank midi file and add a track to it
    mid = mido.MidiFile()
    track = mido.MidiTrack()
    mid.tracks.append(track)

    for item in list1:
        track.append(item[0])

    mid.save('new_song.mid')

    printmessages(mid)

    play_with_pygame('new_song.mid')


if __name__ == '__main__':
    main()

