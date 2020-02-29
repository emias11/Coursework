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


def main():
    # get the list of midi files from regulate_tracks
    output, ticksperbeat = regulate_tracks.main()
    list1 = output

    # create a blank midi file and add a track to it
    mid = mido.MidiFile()
    mid.ticks_per_beat = ticksperbeat
    track = mido.MidiTrack()
    mid.tracks.append(track)

    for i in range(len(list1)):
        message = list1[i][0]
        if i == 0:
            message.time = 0
        else:
            message.time = list1[i][1] - list1[i - 1][1]
        track.append(message)

    mid.save('new_song.mid')

    play_with_pygame('new_song.mid')


if __name__ == '__main__':
    main()

