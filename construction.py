import mido
import pygame
from regulate_tracks import get_all_lists_and_tpb
from probabilities import get_channels_dict
from Markov import get_song_inputs, get_lists_for_all_channels

all_instruments = {1: 'Acoustic Grand Piano', 2: 'Bright Acoustic Piano', 3: 'Electric Grand Piano', 4: 'Honky-tonk Piano', 5: 'Electric Piano 1', 6: 'Electric Piano 2', 7: 'Harpsichord', 8: 'Clavi', 9: 'Celesta', 10: 'Glockenspiel', 11: 'Music Box', 12: 'Vibraphone', 13: 'Marimba', 14: 'Xylophone', 15: 'Tubular Bells', 16: 'Dulcimer', 17: 'Drawbar Organ', 18: 'Percussive Organ', 19: 'Rock Organ', 20: 'Church Organ', 21: 'Reed Organ', 22: 'Accordion', 23: 'Harmonica', 24: 'Tango Accordion', 25: 'Acoustic Guitar (nylon)', 26: 'Acoustic Guitar (steel)', 27: 'Electric Guitar (jazz)', 28: 'Electric Guitar (clean)', 29: 'Electric Guitar (muted)', 30: 'Overdriven Guitar', 31: 'Distortion Guitar', 32: 'Guitar harmonics', 33: 'Acoustic Bass', 34: 'Electric Bass (finger)', 35: 'Electric Bass (pick)', 36: 'Fretless Bass', 37: 'Slap Bass 1', 38: 'Slap Bass 2', 39: 'Synth Bass 1', 40: 'Synth Bass 2', 41: 'Violin', 42: 'Viola', 43: 'Cello', 44: 'Contrabass', 45: 'Tremolo Strings', 46: 'Pizzicato Strings', 47: 'Orchestral Harp', 48: 'Timpani', 49: 'String Ensemble 1', 50: 'String Ensemble 2', 51: 'SynthStrings 1', 52: 'SynthStrings 2', 53: 'Choir Aahs', 54: 'Voice Oohs', 55: 'Synth Voice', 56: 'Orchestra Hit', 57: 'Trumpet', 58: 'Trombone', 59: 'Tuba', 60: 'Muted Trumpet', 61: 'French Horn', 62: 'Brass Section', 63: 'SynthBrass 1', 64: 'SynthBrass 2', 65: 'Soprano Sax', 66: 'Alto Sax', 67: 'Tenor Sax', 68: 'Baritone Sax', 69: 'Oboe', 70: 'English Horn', 71: 'Bassoon', 72: 'Clarinet', 73: 'Piccolo', 74: 'Flute', 75: 'Recorder', 76: 'Pan Flute', 77: 'Blown Bottle', 78: 'Shakuhachi', 79: 'Whistle', 80: 'Ocarina', 81: 'Lead 1 (square)', 82: 'Lead 2 (sawtooth)', 83: 'Lead 3 (calliope)', 84: 'Lead 4 (chiff)', 85: 'Lead 5 (charang)', 86: 'Lead 6 (voice)', 87: 'Lead 7 (fifths)', 88: 'Lead 8 (bass + lead)', 89: 'Pad 1 (new age)', 90: 'Pad 2 (warm)', 91: 'Pad 3 (polysynth)', 92: 'Pad 4 (choir)', 93: 'Pad 5 (bowed)', 94: 'Pad 6 (metallic)', 95: 'Pad 7 (halo)', 96: 'Pad 8 (sweep)', 97: 'FX 1 (rain)', 98: 'FX 2 (soundtrack)', 99: 'FX 3 (crystal)', 100: 'FX 4 (atmosphere)', 101: 'FX 5 (brightness)', 102: 'FX 6 (goblins)', 103: 'FX 7 (echoes)', 104: 'FX 8 (sci-fi)', 105: 'Sitar', 106: 'Banjo', 107: 'Shamisen', 108: 'Koto', 109: 'Kalimba', 110: 'Bag pipe', 111: 'Fiddle', 112: 'Shanai', 113: 'Tinkle Bell', 114: 'Agogo', 115: 'Steel Drums', 116: 'Woodblock', 117: 'Taiko Drum', 118: 'Melodic Tom', 119: 'Synth Drum', 120: 'Reverse Cymbal', 121: 'Guitar Fret Noise', 122: 'Breath Noise', 123: 'Seashore', 124: 'Bird Tweet', 125: 'Telephone Ring', 126: 'Helicopter', 127: 'Applause', 128: 'Gunshot'}


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


def get_songs_msgs(all_mid):
    """
    :param all_mid: a list of all the midi file names you will use
    :return: run regulate tracks on them to get an ordered filtered list of their messages
    """
    output, ticksperbeat = get_all_lists_and_tpb(all_mid)  # input songs as parameters here?
    list1 = output
    return list1


def get_ticksperbeat(all_mid):
    output, ticksperbeat = get_all_lists_and_tpb(all_mid)
    return ticksperbeat


def get_instruments(all_msgs):
    channels_dict = get_channels_dict(all_msgs)
    instruments = []
    programs = channels_dict.keys()
    for program in programs:
        instruments.append(all_instruments[(int(program))+1])
    print(instruments)
    return instruments


def main():
    all_mid = ['ItsBeginningToLookALotLikeChristmas.mid', 'BohemianRhapsody.mid']  # can enter songs here
    list1 = get_songs_msgs(all_mid)
    ticksperbeat = get_ticksperbeat(all_mid)

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


